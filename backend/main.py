import os
import json
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from models import User, MoodEntry, JournalEntry, WellnessLog, UserSettings
from auth import hash_password, verify_password, create_user
from emotion_model import analyze_emotion
from sentiment_model import analyze_sentiment
from gemini_recommender import generate_recommendation

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MoodMentor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AnalyzeRequest(BaseModel):
    text: str
    user_id: int


class JournalRequest(BaseModel):
    user_id: int
    title: str
    content: str
    mood: str = ""


class WellnessRequest(BaseModel):
    user_id: int
    activity: str


class CompanionRequest(BaseModel):
    user_id: int
    message: str


class SettingsRequest(BaseModel):
    user_id: int
    username: str
    email: str
    notifications: bool = True
    daily_reminder: bool = True
    dark_mode: bool = False


class PasswordRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str


# ── Auth Routes ────────────────────────────────────────────


@app.post("/api/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, req.username, req.email, req.password)
    if user is None:
        return {"success": False, "message": "Username or email already exists."}
    return {"success": True, "user": {"id": user.id, "username": user.username, "email": user.email}}


@app.post("/api/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash or ""):
        return {"success": False, "message": "Invalid username or password."}
    return {"success": True, "user": {"id": user.id, "username": user.username, "email": user.email}}


# ── Dashboard ──────────────────────────────────────────────


@app.get("/api/dashboard/{user_id}")
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    mood_entries = (
        db.query(MoodEntry)
        .filter(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.created_at.desc())
        .all()
    )

    journal_entries = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )

    current_mood = mood_entries[0].emotion if mood_entries else "No data"
    mood_score = int(mood_entries[0].emotion_score) if mood_entries else 0

    # Build weekly mood data (last 7 days)
    weekly_mood = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    now = datetime.now()
    for i in range(6, -1, -1):
        day_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        from datetime import timedelta
        day_date = day_date - timedelta(days=i)
        day_entries = [
            e for e in mood_entries
            if e.created_at and e.created_at.date() == day_date.date()
        ]
        avg_score = (
            sum(e.emotion_score for e in day_entries) / len(day_entries)
            if day_entries
            else 50
        )
        weekly_mood.append({
            "day": days[day_date.weekday()],
            "date": day_date.strftime("%b %d"),
            "mood": round(avg_score),
        })

    # Emotion distribution
    emotion_counts = {}
    for entry in mood_entries:
        emo = entry.emotion
        emotion_counts[emo] = emotion_counts.get(emo, 0) + 1
    total_emotions = sum(emotion_counts.values()) or 1
    emotion_distribution = [
        {"emotion": emo, "percentage": round((count / total_emotions) * 100)}
        for emo, count in sorted(emotion_counts.items(), key=lambda x: -x[1])
    ]

    # Today's suggestion
    suggestions = [
        {"title": "Take a mindful walk", "description": "Step outside and take a 10-minute walk. Focus on your surroundings and breathe deeply."},
        {"title": "Practice gratitude", "description": "Write down 3 things you're grateful for today. It can be anything, big or small."},
        {"title": "Deep breathing exercise", "description": "Try 4-7-8 breathing: inhale for 4 seconds, hold for 7, exhale for 8. Repeat 4 times."},
    ]
    today_suggestion = suggestions[now.weekday() % len(suggestions)]

    # Wellness streak
    wellness_logs = (
        db.query(WellnessLog)
        .filter(WellnessLog.user_id == user_id)
        .order_by(WellnessLog.created_at.desc())
        .all()
    )
    streak = 0
    if wellness_logs:
        streak = len(set(
            log.created_at.date()
            for log in wellness_logs
            if log.created_at
        ))

    # Recent journal
    recent_journal = [
        {
            "id": j.id,
            "emoji": {"happy": "😊", "calm": "😌", "sad": "😢", "anxious": "😟", "angry": "😠"}.get(j.mood or "", "📝"),
            "title": j.title,
            "emotion": j.mood or "",
            "time": j.created_at.isoformat() if j.created_at else None,
        }
        for j in journal_entries[:5]
    ]

    return {
        "success": True,
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "stats": {
            "current_mood": current_mood,
            "mood_score": mood_score,
            "journal_entries": len(journal_entries),
            "wellness_streak": streak,
        },
        "weekly_mood": weekly_mood,
        "today_suggestion": today_suggestion,
        "emotion_distribution": emotion_distribution,
        "recent_journal": recent_journal,
    }


# ── Mood Analysis ──────────────────────────────────────────


@app.post("/api/analyze")
def analyze_mood(req: AnalyzeRequest, db: Session = Depends(get_db)):
    emotion_result = analyze_emotion(req.text)
    sentiment_result = analyze_sentiment(req.text)

    try:
        recommendation = generate_recommendation(
            text=req.text,
            emotion=emotion_result["emotion"],
            emotion_score=emotion_result["score"],
            sentiment=sentiment_result["sentiment"],
            sentiment_score=sentiment_result["score"],
        )
    except Exception:
        recommendation = {
            "empathetic_response": "Thank you for sharing how you're feeling.",
            "recommendations": [
                "Take a few deep breaths.",
                "Write down what's on your mind.",
                "Consider talking to someone you trust."
            ],
            "wellness_activity": {
                "title": "Mindful breathing",
                "duration": "5 minutes",
                "description": "Focus on your breath for a few minutes."
            }
        }

    entry = MoodEntry(
        user_id=req.user_id,
        text=req.text,
        emotion=emotion_result["emotion"],
        emotion_score=emotion_result["score"],
        sentiment=sentiment_result["sentiment"],
        sentiment_score=sentiment_result["score"],
        recommendation=json.dumps(recommendation),
    )
    db.add(entry)
    db.commit()

    return {
        "emotion": emotion_result["emotion"],
        "emotion_score": emotion_result["score"],
        "sentiment": sentiment_result["sentiment"],
        "sentiment_score": sentiment_result["score"],
        "recommendation": recommendation,
        "all_emotions": emotion_result["all_emotions"],
    }


# ── Journal ────────────────────────────────────────────────


@app.get("/api/journal/{user_id}")
def get_journals(user_id: int, db: Session = Depends(get_db)):
    entries = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )
    return {
        "journals": [
            {
                "id": j.id,
                "title": j.title,
                "content": j.content,
                "mood": j.mood,
                "created_at": j.created_at.isoformat() if j.created_at else "",
            }
            for j in entries
        ]
    }


@app.post("/api/journal")
def create_journal(req: JournalRequest, db: Session = Depends(get_db)):
    entry = JournalEntry(
        user_id=req.user_id,
        title=req.title,
        content=req.content,
        mood=req.mood if req.mood else None,
    )
    db.add(entry)
    db.commit()
    return {"success": True}


@app.delete("/api/journal/{entry_id}")
def delete_journal(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found.")
    db.delete(entry)
    db.commit()
    return {"success": True}


# ── Analytics ──────────────────────────────────────────────


@app.get("/api/analytics/{user_id}")
def get_analytics(user_id: int, db: Session = Depends(get_db)):
    mood_entries = (
        db.query(MoodEntry)
        .filter(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.created_at.desc())
        .all()
    )

    total = len(mood_entries)
    avg_mood = (
        round(sum(e.emotion_score for e in mood_entries) / total)
        if total
        else 0
    )
    current_mood = mood_entries[0].emotion if mood_entries else "No data"

    # Weekly mood
    weekly_mood = []
    now = datetime.now()
    from datetime import timedelta
    for i in range(6, -1, -1):
        day_date = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
        day_entries = [
            e for e in mood_entries
            if e.created_at and e.created_at.date() == day_date.date()
        ]
        avg = (
            round(sum(e.emotion_score for e in day_entries) / len(day_entries))
            if day_entries
            else 50
        )
        emo = day_entries[0].emotion if day_entries else "neutral"
        weekly_mood.append({"date": day_date.strftime("%b %d"), "mood": avg, "emotion": emo})

    # Emotion distribution
    emotion_counts = {}
    for entry in mood_entries:
        emotion_counts[entry.emotion] = emotion_counts.get(entry.emotion, 0) + 1
    total_emo = sum(emotion_counts.values()) or 1
    emotion_distribution = [
        {"emotion": emo, "percentage": round((c / total_emo) * 100), "count": c}
        for emo, c in sorted(emotion_counts.items(), key=lambda x: -x[1])
    ]

    return {
        "total_entries": total,
        "average_mood": avg_mood,
        "current_mood": current_mood,
        "weekly_mood": weekly_mood,
        "emotion_distribution": emotion_distribution,
    }


# ── Wellness ───────────────────────────────────────────────


@app.get("/api/wellness/{user_id}")
def get_wellness(user_id: int, db: Session = Depends(get_db)):
    logs = (
        db.query(WellnessLog)
        .filter(WellnessLog.user_id == user_id)
        .all()
    )
    return {
        "activities": [{"activity": log.activity} for log in logs]
    }


@app.post("/api/wellness")
def complete_wellness(req: WellnessRequest, db: Session = Depends(get_db)):
    log = WellnessLog(
        user_id=req.user_id,
        activity=req.activity,
        completed=True,
        completed_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    return {"success": True}


# ── Companion ──────────────────────────────────────────────


@app.post("/api/companion")
def companion_chat(req: CompanionRequest):
    from gemini_recommender import client

    # Try Gemini first if available
    if client:
        prompt = f"""You are MoodMentor, a warm and knowledgeable AI wellness companion.
You can answer ANY question — emotional, practical, educational, creative, or casual.
You are empathetic, helpful, and conversational. You give thoughtful, detailed answers.
If the user shares feelings, respond with empathy and support.
If the user asks a question, answer it thoroughly and accurately.
If the user makes a request (songs, books, tips, exercises), give specific, useful suggestions.
Always be warm, caring, and genuine. Keep responses natural and conversational (2-5 sentences, longer if the question deserves it).
Do not use markdown formatting or bullet points.

User message: {req.message}"""

        try:
            response = client.generate_content(prompt)
            reply = response.text.strip()
            if reply and len(reply) > 10:
                return {"reply": reply}
        except Exception as e:
            print(f"Gemini error: {e}")

    # Emotion-aware fallback when Gemini is unavailable
    from companion_chat import _get_companion_reply
    reply = _get_companion_reply(req.message)
    return {"reply": reply}


@app.get("/api/companion/status")
def companion_status():
    """Debug endpoint to check if Gemini is connected and working."""
    from gemini_recommender import client
    gemini_works = False
    gemini_error = None

    if client:
        try:
            response = client.generate_content("Say hi in one word")
            if response.text and len(response.text.strip()) > 0:
                gemini_works = True
        except Exception as e:
            gemini_error = str(e)[:200]

    return {
        "gemini_connected": client is not None,
        "gemini_working": gemini_works,
        "api_key_set": os.getenv("GEMINI_API_KEY") is not None,
        "gemini_error": gemini_error,
        "message": "Gemini is connected and working" if gemini_works else ("Gemini connected but failing: " + (gemini_error or "unknown") if client else "No Gemini - using local fallback")
    }


# ── Settings ───────────────────────────────────────────────


@app.get("/api/settings/{user_id}")
def get_settings(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"success": False, "message": "User not found."}

    settings = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "success": True,
        "user": {"username": user.username, "email": user.email},
        "settings": {
            "notifications": settings.notifications,
            "daily_reminder": settings.daily_reminder,
            "dark_mode": settings.dark_mode,
        },
    }


@app.put("/api/settings")
def update_settings(req: SettingsRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        return {"success": False, "message": "User not found."}

    user.username = req.username
    user.email = req.email

    settings = db.query(UserSettings).filter(UserSettings.user_id == req.user_id).first()
    if not settings:
        settings = UserSettings(user_id=req.user_id)
        db.add(settings)

    settings.notifications = req.notifications
    settings.daily_reminder = req.daily_reminder
    settings.dark_mode = req.dark_mode

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "user": {"id": user.id, "username": user.username, "email": user.email},
    }


@app.put("/api/settings/password")
def change_password(req: PasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        return {"success": False, "message": "User not found."}

    if not verify_password(req.current_password, user.password_hash or ""):
        return {"success": False, "message": "Current password is incorrect."}

    user.password_hash = hash_password(req.new_password)
    db.commit()
    return {"success": True}


@app.delete("/api/settings/account/{user_id}")
def delete_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"success": False, "message": "User not found."}

    db.query(WellnessLog).filter(WellnessLog.user_id == user_id).delete()
    db.query(JournalEntry).filter(JournalEntry.user_id == user_id).delete()
    db.query(MoodEntry).filter(MoodEntry.user_id == user_id).delete()
    db.query(UserSettings).filter(UserSettings.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
