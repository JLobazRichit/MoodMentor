import random as _random

_COMPANION_EMOTION_RESPONSES = {
    "joy": [
        "That's wonderful! I'm really happy to hear you're feeling good. What's been bringing you joy lately?",
        "I love hearing positive energy from you! Happiness like this is worth celebrating. What made your day better?",
        "You sound like you're in a great place right now. That's really lovely. Is there something specific that's making you feel this way?",
        "It warms my heart to hear you're doing well. Positive moments like these are worth savoring. What's been going right?",
        "That's so nice! When you feel this good, it's a great time to think about what's working well in your life. Want to share more?",
    ],
    "sadness": [
        "I hear you, and I want you to know that your feelings are completely valid. Sadness is a natural part of being human. What's been weighing on your mind?",
        "I'm sorry you're going through a tough time. It's okay to not feel okay sometimes. Would you like to talk about what's making you feel this way?",
        "Thank you for trusting me with how you feel. Being sad takes courage to admit. I'm here to listen, take your time.",
        "It sounds like you're carrying a heavy weight right now. You don't have to face it alone. What would help you feel even a little better?",
        "I can sense you're hurting, and I want you to know that it's okay to feel this way. Sometimes just talking about it helps lighten the load.",
    ],
    "anger": [
        "It sounds like something really upset you. Your anger is valid, it means something matters to you. What happened?",
        "I can feel the frustration in your words. Sometimes anger is a sign that a boundary was crossed. Would you like to talk about it?",
        "It's completely okay to feel angry. The important thing is how we channel that energy. What's frustrating you the most right now?",
        "I understand you're upset. Anger can be overwhelming, but it also shows you care deeply. What triggered this feeling?",
        "That sounds really frustrating. Your feelings make sense. Sometimes just venting helps, I'm here to listen without judging.",
    ],
    "fear": [
        "It's completely natural to feel afraid. You're not alone in this, fear is something we all experience. What's worrying you?",
        "I can sense you're feeling anxious. Remember, most of what we worry about never actually happens. What's on your mind?",
        "It takes courage to admit you're scared. You're already braver than you think. Would you like to talk about what's causing this worry?",
        "I hear the worry in your words. Let's take this one step at a time. What feels like the biggest concern right now?",
        "Fear can feel paralyzing, but you're reaching out, and that shows strength. What's making you feel unsafe or uncertain?",
    ],
    "surprise": [
        "Oh wow, that sounds unexpected! How are you feeling about it? Sometimes surprises can bring up a mix of emotions.",
        "That's quite something! Unexpected moments can shake us up. Are you feeling excited, overwhelmed, or something else?",
        "Life sure has a way of surprising us! Take a moment to process, there's no rush to figure everything out right now.",
    ],
    "disgust": [
        "That sounds like a really unpleasant experience. It's okay to feel that way, your reaction shows you have strong values.",
        "I understand this is upsetting. Your feelings of discomfort are valid. Would you like to talk about what happened?",
        "Feeling disgusted means you know what you don't want in your life. That's actually a form of self-awareness.",
    ],
    "calm": [
        "It's nice to hear you're feeling at peace. That's a wonderful state to be in. What helped you find this calm?",
        "Feeling centered is such a gift. Enjoy this moment, you've earned it. Is there anything on your mind you'd like to explore?",
        "I'm glad you're feeling balanced. This is a great time for reflection or simply enjoying the present moment. What would you like to talk about?",
        "That sense of peace you're feeling is something to treasure. What do you think contributed to it?",
    ],
}

_COMPANION_GENERIC = [
    "Thank you for sharing that with me. I'm here to listen and support you. Tell me more about what's going on.",
    "I appreciate you opening up. How long have you been feeling this way?",
    "That sounds like a lot to process. Remember, it's okay to take things one day at a time. What feels most important to you right now?",
    "I'm here for you. Sometimes just having someone to talk to makes a difference. Would you like to explore this feeling further?",
    "Your feelings matter, and so do you. I'm here to listen whenever you need to talk. What else is on your mind?",
    "That's an interesting perspective. How does that make you feel deep down?",
    "I hear you. It sounds like you're going through something meaningful. Would you like to talk about what's behind these feelings?",
    "It takes strength to reach out. Whatever you're going through, you don't have to face it alone. Tell me more.",
    "Sometimes life puts us in difficult situations. What do you think would help you feel better right now?",
    "I'm listening, and I care about how you're doing. What would feel most helpful to talk about?",
]

_COMPANION_GREETINGS = [
    "Hi there! I'm really glad you're here. How are you feeling right now, in this moment?",
    "Welcome back! I'm here whenever you need to talk. What's on your mind today?",
    "Hey! It's good to see you. How has your day been so far?",
    "Hello! I'm here to listen. What's going on in your world right now?",
]

_COMPANION_CHECKINS = [
    "Before we continue, how are you doing right now, in this moment?",
    "I want to make sure you're okay. How are you feeling at this very moment?",
    "Quick check-in: on a scale of 1 to 10, how would you rate your mood right now?",
    "I hope you're being kind to yourself today. How are you really feeling?",
]


def _get_companion_reply(message):
    """Generate an emotion-aware companion reply."""
    from emotion_model import analyze_emotion
    result = analyze_emotion(message)
    emotion = result["emotion"]
    text_lower = message.lower().strip()

    # Check for greetings
    greeting_words = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "greetings", "howdy", "what's up", "sup"]
    if any(text_lower.startswith(gw) for gw in greeting_words) or text_lower in ["hi", "hey", "hello"]:
        return _random.choice(_COMPANION_GREETINGS)

    # Check for check-in phrases
    checkin_words = ["how are you", "how r u", "how're you", "how do you do", "you doing"]
    if any(phrase in text_lower for phrase in checkin_words):
        return _random.choice(_COMPANION_CHECKINS)

    # Use emotion detection for response
    if emotion in _COMPANION_EMOTION_RESPONSES:
        return _random.choice(_COMPANION_EMOTION_RESPONSES[emotion])

    return _random.choice(_COMPANION_GENERIC)
