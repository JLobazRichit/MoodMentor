import os
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}" if api_key else None

# Client object for compatibility - None means no Gemini
class _GeminiClient:
    def __init__(self):
        self.available = api_key is not None

    def generate_content(self, prompt):
        if not self.available:
            raise Exception("No Gemini API key")
        resp = requests.post(
            GEMINI_API_URL,
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Return a simple object with .text attribute
        class _Result:
            pass
        r = _Result()
        r.text = text
        return r

client = _GeminiClient() if api_key else None


# ── Emotion-aware recommendation database ──────────────────
EMOTION_RECOMMENDATIONS = {
    "joy": {
        "empathetic_responses": [
            "It's wonderful to hear that you're feeling happy! Savor this positive moment — you deserve it.",
            "What a great feeling! Let yourself enjoy this happiness fully. These moments are worth treasuring.",
            "That's amazing! Happiness like this is a reminder of how much good there is in your life.",
            "I'm so glad you're experiencing joy right now. Let it fill you up and carry you forward.",
            "Feeling happy is such a gift. Take a moment to appreciate what brought you here.",
        ],
        "recommendations": [
            ["Share your happiness with someone you care about — a quick call or text can brighten both your days.", "Write down three things that made you happy today so you can revisit them later.", "Do something kind for someone else — spreading joy multiplies it."],
            ["Capture this moment in a photo or journal entry — you'll love looking back on it.", "Try a creative activity while you're in this positive headspace — paint, cook, or play music.", "Set a positive intention for tomorrow while your energy is high."],
            ["Celebrate this feeling by doing something you love — take a walk, treat yourself, or dance.", "Use this momentum to tackle something you've been putting off — your energy is powerful right now.", "Practice gratitude by listing five things you appreciate about your life right now."],
        ],
        "wellness_activities": [
            {"title": "Gratitude journaling", "duration": "10 minutes", "description": "Write down five things you're grateful for today. Let the positive feelings deepen as you reflect on what brings you joy."},
            {"title": "Joyful movement", "duration": "15 minutes", "description": "Put on your favorite music and move your body — dance, stretch, or take a lively walk."},
            {"title": "Happy memory collection", "duration": "10 minutes", "description": "Create a collection of your happiest memories — photos, quotes, or drawings. Revisit them whenever you need a boost."},
        ],
    },
    "sadness": {
        "empathetic_responses": [
            "I hear you, and it's okay to feel sad. Your feelings are valid, and you don't have to go through this alone.",
            "Sadness can be heavy, but it also means you care deeply. Be gentle with yourself right now.",
            "I'm sorry you're going through a tough time. Remember that feelings are temporary, even when they feel overwhelming.",
            "It takes courage to express how you feel. Thank you for sharing — I'm here to listen without judgment.",
            "Sadness is a natural part of life. Allow yourself to feel it, but know that brighter days are ahead.",
        ],
        "recommendations": [
            ["Reach out to a friend or family member — even a short conversation can help you feel less alone.", "Write about what's making you sad in your journal — getting thoughts on paper can bring clarity.", "Do one small thing that usually brings you comfort — a warm drink, a cozy blanket, or a favorite song."],
            ["Allow yourself to cry if you need to — it's your body's way of releasing emotional pain.", "Take a gentle walk outside, even for just 10 minutes — nature has a calming effect on the mind.", "Listen to music that matches your mood, then slowly shift to something more uplifting."],
            ["Practice self-compassion — talk to yourself the way you would talk to a dear friend.", "Create a comfort playlist of songs, videos, or memories that make you feel safe and loved.", "Try a breathing exercise: breathe in for 4 counts, hold for 4, exhale for 6. Repeat five times."],
        ],
        "wellness_activities": [
            {"title": "Comfort breathing", "duration": "5 minutes", "description": "Find a quiet spot, close your eyes, and breathe deeply. Inhale peace, exhale pain. You are safe in this moment."},
            {"title": "Self-care check-in", "duration": "10 minutes", "description": "Ask yourself: What do I need right now? A warm meal? Rest? A hug? Honor that need, even in a small way."},
            {"title": "Gentle stretching", "duration": "10 minutes", "description": "Do a series of slow, gentle stretches. Focus on releasing tension from your shoulders, neck, and chest."},
        ],
    },
    "anger": {
        "empathetic_responses": [
            "It's completely understandable to feel angry — your feelings are valid. Let's find a healthy way to process this.",
            "Anger often signals that a boundary has been crossed. Acknowledging it is the first step to addressing it.",
            "I can see this situation really frustrated you. Taking a moment to breathe can help you respond thoughtfully.",
            "Your anger makes sense given what you're dealing with. You have every right to feel this way.",
            "Anger is a powerful emotion. When channeled well, it can become a force for positive change.",
        ],
        "recommendations": [
            ["Take five slow, deep breaths before responding — this gives your rational mind a chance to catch up.", "Write an uncensored letter about how you feel, then tear it up — release the intensity without consequences.", "Physical movement helps: try push-ups, a brisk walk, or squeezing a stress ball."],
            ["Step away from the situation for 10 minutes — distance gives you perspective and calms your nervous system.", "Name the specific emotion beneath the anger — is it hurt, fear, or disappointment? Understanding helps.", "Listen to energetic music or nature sounds to redirect your emotional energy."],
            ["Practice progressive muscle relaxation: tense each muscle group for 5 seconds, then release.", "Draw or scribble your anger on paper — use colors that match how you feel.", "Remind yourself: I can feel angry and still choose how I respond."],
        ],
        "wellness_activities": [
            {"title": "Cool-down walk", "duration": "10 minutes", "description": "Step outside and walk at a brisk pace. Focus on your footsteps and breathing. Let each step carry away tension."},
            {"title": "Anger release journaling", "duration": "10 minutes", "description": "Write everything you're feeling without filtering. Don't worry about grammar — just let it pour out. Then take a deep breath."},
            {"title": "Body scan relaxation", "duration": "8 minutes", "description": "Lie down and slowly scan from your toes to your head. Notice where you're holding tension and consciously release it."},
        ],
    },
    "fear": {
        "empathetic_responses": [
            "It's natural to feel afraid when facing uncertainty. You're brave for acknowledging this feeling.",
            "Fear is your mind trying to protect you. You don't have to face this alone — take it one step at a time.",
            "I understand this feels overwhelming. Remember, you've overcome challenges before and you can do it again.",
            "Fear can feel paralyzing, but you're stronger than you think. Let's focus on what you can control.",
            "It's okay to be scared. Courage isn't the absence of fear — it's choosing to move forward despite it.",
        ],
        "recommendations": [
            ["Ground yourself with the 5-4-3-2-1 technique: name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste.", "Write down your specific fears — seeing them on paper often makes them feel more manageable.", "Talk to someone you trust about what's worrying you — sharing fears reduces their power."],
            ["Practice box breathing: inhale for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat.", "Focus on one small, manageable step you can take right now — don't try to solve everything at once.", "Remind yourself of past challenges you've successfully navigated — you have a track record of resilience."],
            ["Create a worry window — give yourself 10 minutes to worry, then consciously set those thoughts aside.", "Use positive self-talk: replace 'What if something goes wrong?' with 'What if everything goes right?'", "Do something that makes you feel capable and strong — even organizing your space can help."],
        ],
        "wellness_activities": [
            {"title": "Grounding meditation", "duration": "5 minutes", "description": "Sit comfortably and focus on your breath. With each exhale, imagine releasing one worry. You are here, you are safe."},
            {"title": "Safety visualization", "duration": "8 minutes", "description": "Close your eyes and picture a place where you feel completely safe and at peace. Notice every detail."},
            {"title": "Progressive relaxation", "duration": "10 minutes", "description": "Starting from your toes, tense each muscle group for 5 seconds, then release. Work your way up to your face."},
        ],
    },
    "surprise": {
        "empathetic_responses": [
            "Wow, that sounds unexpected! Surprises can be a lot to process — take a moment to absorb it all.",
            "That's quite a revelation! It's natural to feel a mix of emotions when something unexpected happens.",
            "Unexpected moments can shift our perspective in powerful ways. How are you feeling about this?",
            "Life has a way of keeping us on our toes! Allow yourself to sit with this surprise for a bit.",
            "Surprises remind us that we can't predict everything — and that's part of what makes life interesting.",
        ],
        "recommendations": [
            ["Give yourself time to process — you don't need to react or decide anything right away.", "Talk to someone about what happened — sharing can help you make sense of your feelings.", "Write down your initial reaction and revisit it in a day — your perspective may evolve."],
            ["Take a few deep breaths to center yourself before making any decisions.", "Consider both the positive and negative aspects of this surprise — it may open new doors.", "Practice flexibility by accepting that uncertainty is a natural part of life."],
            ["Use this as an opportunity for growth — unexpected events often teach us about ourselves.", "Meditate for 5 minutes to find clarity amid the emotional swirl.", "Channel your energy into something creative — surprises often spark inspiration."],
        ],
        "wellness_activities": [
            {"title": "Mindful reflection", "duration": "10 minutes", "description": "Sit quietly and reflect on what surprised you. Without judging, observe how your body and mind are responding."},
            {"title": "Perspective shift journaling", "duration": "10 minutes", "description": "Write about the surprise from three perspectives: now, tomorrow, and a year from now."},
            {"title": "Breath work reset", "duration": "5 minutes", "description": "Inhale for 4, hold for 7, exhale for 8. Let each breath ground you in the present."},
        ],
    },
    "disgust": {
        "empathetic_responses": [
            "That sounds really unpleasant. It's okay to feel disgusted — it's your body's way of protecting you.",
            "I understand this is upsetting. Your reaction is completely valid given what you've experienced.",
            "Feeling disgusted shows you have strong values and boundaries. That's actually a strength.",
            "It's natural to feel repulsed by certain things. Acknowledging it is the first step to processing it.",
            "Your discomfort matters. Take a moment to care for yourself after this experience.",
        ],
        "recommendations": [
            ["Take a few moments to distance yourself from the trigger — step outside or move to a different space.", "Cleanse your environment — tidy up, light a candle, or open a window for fresh air.", "Write about what triggered this feeling to understand your boundaries better."],
            ["Practice a grounding exercise to bring your focus back to the present moment.", "Do something that restores your sense of comfort — a warm shower or washing your hands.", "Remind yourself that this feeling will pass — it's your body's alarm system doing its job."],
            ["Engage your senses with something pleasant — calming music, a nice scent, or a warm drink.", "Talk about what happened with someone you trust — verbalizing helps process the emotion.", "Practice self-compassion — your reaction shows you care about your values."],
        ],
        "wellness_activities": [
            {"title": "Cleansing ritual", "duration": "10 minutes", "description": "Wash your hands mindfully, imagining unpleasant feelings washing away. Follow with a comforting activity."},
            {"title": "Nature immersion", "duration": "15 minutes", "description": "Step into nature and focus on the beauty around you — fresh air, green leaves, birdsong."},
            {"title": "Comfort creation", "duration": "10 minutes", "description": "Create a small comfort space — soft lighting, a warm blanket, a gentle scent. Feel safe and at ease."},
        ],
    },
    "calm": {
        "empathetic_responses": [
            "It's wonderful that you're feeling calm and centered. This inner peace is a strength you can draw on.",
            "Being at peace is a beautiful state. Take a moment to appreciate this balance in your life.",
            "Serenity like this is worth nurturing. You've found a good place — let yourself enjoy it.",
            "Feeling calm and content is a sign of emotional wellbeing. You're doing great.",
            "This peaceful state is a resource you can return to whenever you need it. Remember how it feels.",
        ],
        "recommendations": [
            ["Use this calm state to reflect on what's going well in your life — gratitude deepens peace.", "Set a positive intention for the rest of your day while your mind is clear and focused.", "Share your peaceful energy with someone who might need it — a kind word can make someone's day."],
            ["Journal about what helped you reach this calm state so you can recreate it when needed.", "Practice mindful observation — notice the details around you with curiosity and appreciation.", "Channel this calm focus into a creative project or meaningful task."],
            ["Take a slow, intentional walk and appreciate the world around you.", "Write a letter of appreciation to someone who has positively impacted your life.", "Use this clarity to make a decision you've been putting off — your mind is at its best right now."],
        ],
        "wellness_activities": [
            {"title": "Loving-kindness meditation", "duration": "10 minutes", "description": "Send wishes of happiness and peace to yourself, then to someone you love, then to everyone."},
            {"title": "Mindful observation", "duration": "10 minutes", "description": "Pick an object and observe it with full attention for 5 minutes. Notice every detail."},
            {"title": "Gratitude reflection", "duration": "10 minutes", "description": "Sit quietly and reflect on three things you're grateful for. Feel the warmth of appreciation."},
        ],
    },
}


# ── Context-aware keyword detection ────────────────────────
CONTEXT_KEYWORDS = {
    "work": ["work", "job", "career", "boss", "colleague", "office", "promotion", "meeting", "deadline", "project", "manager", "fired", "resign"],
    "relationships": ["love", "partner", "relationship", "friend", "family", "marriage", "dating", "breakup", "divorce", "boyfriend", "girlfriend", "husband", "wife", "parent", "child"],
    "health": ["health", "sick", "illness", "pain", "doctor", "hospital", "diagnosis", "medication", "symptom", "cancer", "chronic", "therapy"],
    "studies": ["exam", "study", "school", "college", "university", "test", "grade", "homework", "assignment", "class", "professor"],
    "sleep": ["sleep", "insomnia", "rest", "tired", "exhausted", "nightmare", "bed", "morning", "awake"],
    "money": ["money", "financial", "bills", "debt", "income", "expense", "budget", "afford", "savings", "broke", "rent"],
    "self": ["myself", "self", "body", "image", "worth", "confidence", "identity", "purpose", "meaning", "alone", "empty"],
}


def _detect_context(text):
    text_lower = text.lower()
    scores = {}
    for ctx, kws in CONTEXT_KEYWORDS.items():
        count = sum(1 for kw in kws if kw in text_lower)
        if count > 0:
            scores[ctx] = count
    return max(scores, key=scores.get) if scores else "general"


def _get_contextual_empathy(emotion, context, text):
    emotion_data = EMOTION_RECOMMENDATIONS.get(emotion, EMOTION_RECOMMENDATIONS["calm"])
    base = random.choice(emotion_data["empathetic_responses"])
    prefixes = {
        "work": "Work-related stress can feel relentless. ",
        "relationships": "Relationships are deeply personal. ",
        "health": "Health concerns weigh heavily on the mind. ",
        "studies": "Academic pressure can feel overwhelming. ",
        "sleep": "Sleep struggles affect everything else. ",
        "money": "Financial worries are among the most stressful. ",
        "self": "Self-reflection takes courage. ",
    }
    if context in prefixes:
        return prefixes[context] + base
    return base


def _get_contextual_recommendations(emotion, context):
    emotion_data = EMOTION_RECOMMENDATIONS.get(emotion, EMOTION_RECOMMENDATIONS["calm"])
    base = random.choice(emotion_data["recommendations"])
    context_tips = {
        "work": ["Consider setting a clear boundary between work time and personal time today.", "Your job title doesn't define your worth as a person.", "Try a brief desk meditation — even 60 seconds of focused breathing helps."],
        "relationships": ["Remember that you cannot control others, only how you respond.", "Healthy relationships require both connection and personal space.", "Consider writing down what you need from this relationship."],
        "health": ["Be patient with your body — healing takes time and self-compassion.", "Focus on what you CAN control: rest, nutrition, and gentle movement.", "Consider reaching out to a healthcare professional if symptoms persist."],
        "studies": ["Break your study sessions into 25-minute focused blocks with 5-minute breaks.", "Remember that one exam doesn't define your intelligence or future.", "Talk to a classmate or teacher — you don't have to struggle alone."],
        "sleep": ["Tonight, try putting screens away 30 minutes before bed.", "Create a calming bedtime routine — warm tea, gentle stretching, deep breathing.", "If your mind races at night, keep a notepad by your bed to write down worries."],
        "money": ["Financial stress is real and valid. Focus on one small step you can take today.", "Many communities offer free financial counseling — you don't have to figure this out alone.", "Track your spending for a week — awareness is the first step to change."],
        "self": ["You are more than your worst moment. Practice speaking to yourself with kindness.", "Try placing your hand on your heart and saying 'I am enough.'", "Explore what matters most to you — purpose often emerges from reflection."],
    }
    if context in context_tips:
        tips = context_tips[context]
        return [random.choice(tips)] + base[:2]
    return base


def _get_contextual_activity(emotion, context):
    emotion_data = EMOTION_RECOMMENDATIONS.get(emotion, EMOTION_RECOMMENDATIONS["calm"])
    context_activities = {
        "work": {"title": "Workplace reset", "duration": "5 minutes", "description": "Step away from your desk. Stretch your arms overhead, roll your shoulders, and take 5 deep breaths."},
        "relationships": {"title": "Heart-centered breathing", "duration": "8 minutes", "description": "Place your hand over your heart. Breathe slowly and imagine warmth spreading from your chest."},
        "health": {"title": "Body appreciation", "duration": "5 minutes", "description": "Place your hand on the part of your body that needs attention. Thank it for carrying you this far."},
        "studies": {"title": "Study break reset", "duration": "5 minutes", "description": "Close your books, stand up, and do 10 jumping jacks. Then sit quietly for 2 minutes and breathe."},
        "sleep": {"title": "Sleep preparation ritual", "duration": "10 minutes", "description": "Dim the lights, put away screens, and listen to soft music. Take a warm shower, then breathe slowly."},
        "money": {"title": "Abundance meditation", "duration": "8 minutes", "description": "Close your eyes and visualize yourself free from financial worry. Feel the relief and peace."},
        "self": {"title": "Mirror affirmation", "duration": "5 minutes", "description": "Look at yourself in the mirror and say three things you appreciate about who you are inside."},
    }
    if context in context_activities:
        return context_activities[context]
    return random.choice(emotion_data["wellness_activities"])


def generate_recommendation(text, emotion, emotion_score, sentiment, sentiment_score):
    prompt = f"""
You are MoodMentor, an empathetic AI emotional wellness assistant.
Analyze the user's emotional situation and provide personalized, practical and supportive recommendations.

User message: {text}
Detected emotion: {emotion}
Emotion confidence: {emotion_score:.1f}%
Detected sentiment: {sentiment}
Sentiment confidence: {sentiment_score:.1f}%

Return ONLY valid JSON with this structure:
{{
    "empathetic_response": "A short supportive response to the user's situation.",
    "recommendations": ["First recommendation", "Second recommendation", "Third recommendation"],
    "wellness_activity": {{"title": "Activity name", "duration": "10 minutes", "description": "How to do the activity."}}
}}

Rules: No Markdown, no bold, no numbered lists. Keep empathetic response under 3 sentences. Exactly 3 recommendations related to the user's message. Be supportive and non-judgmental. Return JSON only.
"""

    if not client:
        context = _detect_context(text)
        return {
            "empathetic_response": _get_contextual_empathy(emotion, context, text),
            "recommendations": _get_contextual_recommendations(emotion, context),
            "wellness_activity": _get_contextual_activity(emotion, context),
        }

    try:
        response = client.generate_content(prompt)
    except Exception:
        context = _detect_context(text)
        return {
            "empathetic_response": _get_contextual_empathy(emotion, context, text),
            "recommendations": _get_contextual_recommendations(emotion, context),
            "wellness_activity": _get_contextual_activity(emotion, context),
        }

    response_text = response.text.strip()
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        context = _detect_context(text)
        return {
            "empathetic_response": _get_contextual_empathy(emotion, context, text),
            "recommendations": _get_contextual_recommendations(emotion, context),
            "wellness_activity": _get_contextual_activity(emotion, context),
        }
