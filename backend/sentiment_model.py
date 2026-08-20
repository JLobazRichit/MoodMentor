"""
Lightweight sentiment analysis - delegates to emotion_model.
Kept as separate import for backward compatibility.
"""
from emotion_model import analyze_sentiment


def analyze_sentiment_standalone(text: str):
    return analyze_sentiment(text)
