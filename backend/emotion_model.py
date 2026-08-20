"""
Lightweight emotion analysis using keyword matching.
No ML models needed - works on free tier hosting.
"""

EMOTION_KEYWORDS = {
    "joy": ["happy", "glad", "excited", "wonderful", "great", "love", "amazing", "fantastic", "cheerful", "delighted", "blessed", "grateful", "thankful", "proud", "fun", "enjoy", "smile", "laugh", "celebrate"],
    "sadness": ["sad", "unhappy", "depressed", "lonely", "miss", "cry", "tears", "heartbroken", "grief", "loss", "hopeless", "empty", "hurt", "pain", "suffering", "miserable", "gloomy", "down"],
    "anger": ["angry", "mad", "furious", "rage", "hate", "frustrated", "annoyed", "irritated", "outraged", "livid", "bitter", "resentful", "hostile", "aggressive"],
    "fear": ["afraid", "scared", "anxious", "worried", "nervous", "panic", "terrified", "dread", "frightened", "uneasy", "tense", "stressed", "overwhelmed"],
    "surprise": ["surprised", "shocked", "amazed", "astonished", "unexpected", "wow", "unbelievable", "sudden", "startled"],
    "disgust": ["disgusted", "gross", "revolting", "sick", "nasty", "awful", "terrible", "horrible", "dreadful"],
    "neutral": ["okay", "fine", "alright", "normal", "nothing", "usual", "regular", "calm", "peaceful", "relaxed", "content"],
}

SENTIMENT_POSITIVE = ["happy", "love", "great", "amazing", "wonderful", "good", "best", "beautiful", "thank", "grateful", "blessed", "excited", "proud", "glad", "enjoy", "smile", "laugh", "cheerful", "fantastic", "perfect", "awesome", "excellent", "nice", "pleasant", "joyful", "hopeful", "confident"]

SENTIMENT_NEGATIVE = ["sad", "bad", "terrible", "horrible", "hate", "angry", "mad", "cry", "hurt", "pain", "suffer", "depressed", "anxious", "worried", "scared", "afraid", "lonely", "miss", "lost", "hopeless", "miserable", "awful", "worst", "frustrated", "annoyed", "stressed", "overwhelmed", "negative", "fail", "failure", "disappointed"]


def analyze_emotion(text: str):
    text_lower = text.lower()
    words = text_lower.split()
    scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        count = sum(1 for word in words if any(kw in word for kw in keywords))
        scores[emotion] = count
    total = sum(scores.values()) or 1
    all_emotions = [
        {"label": emo, "score": round((count / total) * 100, 2)}
        for emo, count in sorted(scores.items(), key=lambda x: -x[1])
    ]
    best = all_emotions[0] if all_emotions else {"label": "neutral", "score": 50.0}
    return {"emotion": best["label"], "score": best["score"], "all_emotions": all_emotions}


def analyze_sentiment(text: str):
    text_lower = text.lower()
    words = text_lower.split()
    pos_count = sum(1 for w in words if any(kw in w for kw in SENTIMENT_POSITIVE))
    neg_count = sum(1 for w in words if any(kw in w for kw in SENTIMENT_NEGATIVE))
    total = pos_count + neg_count or 1
    if pos_count > neg_count:
        return {"sentiment": "POSITIVE", "score": round((pos_count / total) * 100, 2)}
    elif neg_count > pos_count:
        return {"sentiment": "NEGATIVE", "score": round((neg_count / total) * 100, 2)}
    else:
        return {"sentiment": "NEUTRAL", "score": 50.0}
