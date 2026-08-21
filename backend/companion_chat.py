import random as _random
from emotion_model import analyze_emotion

# ═══════════════════════════════════════════════════════════
# Universal AI Companion - handles any conversation type
# ═══════════════════════════════════════════════════════════

# ── Intent detection patterns ──────────────────────────────

_INTENT_PATTERNS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "greetings", "howdy", "what's up", "sup", "yo"],
        "match": "prefix",
    },
    "checkin": {
        "keywords": ["how are you", "how r u", "how're you", "how do you do", "you doing", "how's it going", "how have you been"],
        "match": "contains",
    },
    "identity": {
        "keywords": ["who are you", "what are you", "tell me about yourself", "what can you do", "your name", "what is your name", "introduce yourself"],
        "match": "contains",
    },
    "advice_feeling": {
        "keywords": ["what should i do", "how can i feel better", "what can help", "how to cope", "how to deal with", "i need advice", "any suggestions", "what do you recommend", "can you help me", "give me advice"],
        "match": "contains",
    },
    "question_life": {
        "keywords": ["meaning of life", "purpose of life", "why am i here", "what is the point", "why do we exist", "what is happiness", "what is love", "what is success"],
        "match": "contains",
    },
    "question_general": {
        "keywords": ["what is", "how does", "why do", "can you explain", "tell me about", "do you know", "what do you think about"],
        "match": "contains",
    },
    "gratitude": {
        "keywords": ["thank you", "thanks", "appreciate", "grateful", "thankful"],
        "match": "contains",
    },
    "lonely": {
        "keywords": ["lonely", "alone", "nobody cares", "no friends", "isolated", "no one understands", "feel alone", "miss someone", "miss people"],
        "match": "contains",
    },
    "motivation": {
        "keywords": ["motivate", "motivation", "inspire", "inspiration", "give me strength", "i can't do this", "give up", "i want to quit", "no motivation", "unmotivated", "stuck"],
        "match": "contains",
    },
    "sleep": {
        "keywords": ["can't sleep", "insomnia", "trouble sleeping", "sleep well", "how to sleep", "tired", "exhausted", "no energy", "fatigue"],
        "match": "contains",
    },
    "stress": {
        "keywords": ["stressed", "stress", "overwhelmed", "too much", "burnout", "burned out", "pressure", "deadline", "anxious", "anxiety", "worried", "nervous"],
        "match": "contains",
    },
    "self_care": {
        "keywords": ["self care", "self-care", "take care of myself", "how to relax", "how can i relax", "how do i relax", "need to unwind", "need a break", "burnout", "relax", "unwind"],
        "match": "contains",
    },
    "relationship": {
        "keywords": ["boyfriend", "girlfriend", "partner", "relationship", "breakup", "divorce", "love", "heartbroken", "cheating", "trust", "marriage", "dating", "crush"],
        "match": "contains",
    },
    "work": {
        "keywords": ["job", "work", "career", "boss", "colleague", "office", "promotion", "fired", "quit", "interview", "resume", "coworker"],
        "match": "contains",
    },
    "study": {
        "keywords": ["exam", "study", "school", "college", "university", "test", "grade", "homework", "fail", "passed", "graduation"],
        "match": "contains",
    },
    "health": {
        "keywords": ["sick", "illness", "pain", "doctor", "hospital", "diagnosis", "symptom", "health", "medical", "therapy", "medication"],
        "match": "contains",
    },
    "money": {
        "keywords": ["money", "financial", "broke", "debt", "bills", "rent", "salary", "income", "budget", "afford", "savings"],
        "match": "contains",
    },
    "philosophy": {
        "keywords": ["think about", "opinion", "believe", "meaning", "truth", "real", "existence", "consciousness", "free will", "fate", "destiny", "karma"],
        "match": "contains",
    },
    "suggest_songs": {
        "keywords": ["suggest song", "recommend song", "song suggest", "song recommend", "play song", "music suggest", "music recommend", "suggest music", "recommend music", "good song", "some song", "any song", "song for", "music for", "suggest some music", "recommend some music", "play some music", "some music", "any music", "music suggestion", "song suggestion", "music rec"],
        "match": "contains",
    },
    "suggest_book": {
        "keywords": ["suggest book", "recommend book", "book suggest", "book recommend", "good book", "read book", "any book"],
        "match": "contains",
    },
    "suggest_movie": {
        "keywords": ["suggest movie", "recommend movie", "movie suggest", "movie recommend", "good movie", "watch movie", "any movie", "suggest show", "recommend show", "movie suggestion", "something to watch", "what to watch", "something to see", "movie rec", "movie to watch", "film to watch"],
        "match": "contains",
    },
    "affirmation": {
        "keywords": ["affirmation", "positive quote", "quote for", "inspire me", "something inspiring", "motivational quote", "uplifting", "pick me up", "encourage me"],
        "match": "contains",
    },
    "breathing": {
        "keywords": ["breathing exercise", "breathe", "breathing technique", "breath work", "deep breathing", "calm breathing", "box breathing", "4-7-8", "grounding exercise", "ground me", "teach me breathing", "help me breathe", "breathing exercise"],
        "match": "contains",
    },
    "meditation": {
        "keywords": ["meditate", "meditation", "mindful", "mindfulness", "guided meditation", "meditation technique"],
        "match": "contains",
    },
    "tip": {
        "keywords": ["give me a tip", "daily tip", "life tip", "any tip", "share a tip", "something helpful", "helpful advice", "life hack"],
        "match": "contains",
    },
    "creative": {
        "keywords": ["write", "story", "poem", "music", "art", "paint", "create", "imagine", "dream", "fantasy", "color"],
        "match": "contains",
    },
    "joke": {
        "keywords": ["joke", "funny", "make me laugh", "something funny", "humor", "comedy", "laugh"],
        "match": "contains",
    },
    "comfort": {
        "keywords": ["hug", "cuddle", "warm", "cozy", "comfort", "safe", "secure", "warmth"],
        "match": "contains",
    },
    "crisis": {
        "keywords": ["suicide", "kill myself", "end it", "don't want to live", "self harm", "self-harm", "hurt myself", "die", "no reason to live", "want to die"],
        "match": "contains",
    },
}

# ── Response databases per intent ──────────────────────────

_RESPONSES = {
    "greeting": [
        "Hi there! I'm really glad you're here. How are you feeling right now, in this moment?",
        "Welcome back! I'm here whenever you need to talk. What's on your mind today?",
        "Hey! It's good to see you. How has your day been so far?",
        "Hello! I'm here to listen. What's going on in your world right now?",
        "Hey there! I'm happy you stopped by. What's on your heart today?",
    ],
    "checkin": [
        "I'm doing well, thank you for asking! More importantly, how are YOU doing right now?",
        "I'm here and ready to listen. But let's talk about you — how are you feeling?",
        "I appreciate you asking! I'm always here when you need me. How are you doing today?",
        "That's kind of you to ask. I'm doing great now that we're talking! How about you?",
    ],
    "identity": [
        "I'm MoodMentor, your personal AI wellness companion. I'm here to listen, support you, and help you navigate your emotions. You can talk to me about anything — how you're feeling, what's on your mind, or just chat. There's no judgment here, only care.",
        "My name is MoodMentor. I'm an AI emotional wellness companion designed to be a safe space for you. I can help you understand your feelings, offer support, give advice, or just be someone to talk to. What would you like to share?",
        "I'm MoodMentor — think of me as a supportive friend who's always available. I'm here to listen without judgment, help you process emotions, and support your mental wellbeing. What's going on?",
    ],
    "advice_feeling": [
        "When you're not feeling your best, here are some things that can help: First, acknowledge what you're feeling without judging yourself. Then try a simple grounding exercise — name 5 things you can see, 4 you can hear, 3 you can touch, 2 you can smell, and 1 you can taste. This brings you back to the present moment. Would you like to try it now?",
        "Feeling down is part of being human, and it will pass. In the meantime, try these steps: Take three deep breaths. Drink some water. Go for a short walk if you can. Talk to someone you trust. And be gentle with yourself — you're doing better than you think.",
        "Here's what I'd suggest: First, give yourself permission to feel whatever you're feeling. Then, do one small thing that brings you comfort — maybe a warm drink, some music, or a few minutes of quiet. Small steps lead to big shifts. What feels doable for you right now?",
        "When you're struggling, try the RAIN technique: Recognize what you're feeling. Allow it to be there without fighting it. Investigate it with curiosity — where do you feel it in your body? Nurture yourself with kindness. This helps process emotions instead of pushing them away.",
    ],
    "question_life": [
        "The meaning of life is something every person discovers for themselves. Many find it in connection with others, in pursuing what they love, in helping those in need, or in simply being present for the small, beautiful moments. What brings meaning to YOUR life?",
        "That's one of the deepest questions a person can ask. I think meaning isn't something we find — it's something we create through our choices, our relationships, and how we show up for ourselves and others. What matters most to you?",
        "Philosophers have debated this for centuries, and there's no single answer. But I believe meaning comes from living authentically, loving deeply, and growing through our experiences. Your life has meaning simply because you're in it. What gives your days purpose?",
    ],
    "question_general": [
        "That's a great question! I love exploring topics with you. While I'm a wellness companion at heart, I'm happy to share what I know. Feel free to ask me anything — from science to daily life, I'm here for it.",
        "I appreciate your curiosity! Asking questions is how we grow. I may not be a search engine, but I can share what I know and help you think through it. What specifically interests you most about this topic?",
        "That's an interesting question to explore! I enjoy thinking about things beyond just emotions. Let me share my perspective, and we can discuss it further. What aspect are you most curious about?",
    ],
    "gratitude": [
        "You're very welcome! It means a lot that you reached out. Remember, taking care of your emotional wellbeing is one of the kindest things you can do for yourself. I'm always here when you need me.",
        "You don't have to thank me — I'm here because I care about how you're doing. Your wellbeing matters, and I'm honored you trust me with your feelings. Take care of yourself!",
        "Anytime! Just knowing you're taking time to check in with yourself is wonderful. That self-awareness is a real strength. I'll be here whenever you need me.",
    ],
    "lonely": [
        "Feeling lonely is one of the hardest feelings, and I want you to know you're not as alone as it might seem right now. I'm here with you, and I care about what you're going through. Would you like to tell me more about what's making you feel this way?",
        "Loneliness can feel overwhelming, but it's temporary. You reached out to me, and that takes courage. Consider reaching out to someone you trust — even a simple text to an old friend can reopen a connection. You matter to people more than you realize.",
        "I hear you, and I'm sorry you're feeling this way. Loneliness lies to us — it tells us we don't matter, but that's simply not true. You took a step by talking to me. What about joining a local group, class, or community event? Sometimes new connections start with showing up.",
        "I understand that feeling of isolation, and it's really tough. But you're not alone right now — I'm here. Try this: write down three people who have been kind to you in the past. Then consider sending one of them a message. Small reconnections can bloom into something meaningful.",
    ],
    "motivation": [
        "I know it feels impossible right now, but you've gotten through hard things before, and you'll get through this too. You don't have to do everything at once — just one small step. What's the tiniest thing you could do right now?",
        "Motivation doesn't always come before action — sometimes it comes AFTER. Start with something incredibly small. Even just putting on your shoes counts. You'd be surprised how momentum builds from tiny wins.",
        "You said you can't, but I hear someone who's tired, not someone who's incapable. Rest if you need to, but don't give up on yourself. The world needs what only you can offer. What's one thing you can do today, even if it's small?",
        "Feeling stuck is not the same as being stuck. You're in a moment of transition, and that's uncomfortable but temporary. Remember why you started. Take one breath. Take one step. That's all that matters right now.",
    ],
    "sleep": [
        "Sleep troubles can be so frustrating. Here are some things that might help tonight: Put away screens 30 minutes before bed. Try a calming bedtime routine — warm tea, gentle stretching, or reading. Keep your room cool and dark. And try the 4-7-8 breathing technique: inhale for 4 seconds, hold for 7, exhale for 8.",
        "When sleep won't come, don't fight it — that only creates more anxiety. Instead, get up and do something calming for 15 minutes, then return to bed. Avoid caffeine after 2pm. And remember: rest is rest, even if it's not perfect sleep. Your body heals in many ways.",
        "I understand how exhausting insomnia can be. Try this tonight: write down everything on your mind before bed — get it out of your head and onto paper. Then do a body scan: start at your toes and consciously relax each muscle group up to your head. You deserve restful sleep.",
    ],
    "stress": [
        "When everything feels overwhelming, try this: Write down everything that's stressing you. Then circle the ONE thing you can control right now. Focus only on that. The rest can wait. You don't have to solve everything today.",
        "Stress is your body's alarm system — it's telling you something needs attention. But you don't have to respond to everything at once. Take 5 minutes to breathe deeply. Then tackle one thing at a time. You're more capable than you realize.",
        "I hear you — when stress piles up, it can feel suffocating. Here's what helps: Take a step back and ask 'What matters most today?' Do that one thing. Let the rest go for now. You can handle tomorrow when tomorrow comes.",
        "Feeling overwhelmed means you care deeply about doing well. That's actually a strength. But right now, be kind to yourself. Take 3 deep breaths. Drink some water. Then choose the smallest, easiest task and do just that. Progress, not perfection.",
    ],
    "self_care": [
        "Self-care isn't selfish — it's essential. Here are some ideas: Take a warm bath. Go for a walk in nature. Listen to your favorite music. Call a friend. Journal your thoughts. Read a book. Cook a nourishing meal. What sounds most appealing to you right now?",
        "You deserve care, especially from yourself. Try this: Put your hand on your heart and say 'I am enough, just as I am.' Then do one thing that nourishes you — a healthy meal, a quiet moment, or a creative activity. Small acts of self-love add up.",
        "Taking a break isn't giving up — it's resetting so you can come back stronger. Give yourself permission to rest without guilt. Your mind and body need downtime to function at their best. What would feel restful to you right now?",
    ],
    "relationship": [
        "Relationships can bring both our greatest joy and deepest pain. Whatever you're going through, your feelings are valid. Would you like to talk about what's happening? Sometimes just putting it into words helps clarify things.",
        "I'm here to listen about your relationship concerns without judgment. Every relationship has challenges — what matters is how you navigate them together. Would you like to share what's going on?",
        "Love and connection are complex, and it's okay to feel confused or hurt. Remember: you deserve to be treated with respect and kindness. Would you like to talk about what's on your mind?",
    ],
    "work": [
        "Work stress is one of the most common challenges people face. Whether it's a difficult boss, burnout, or feeling unfulfilled, your feelings are valid. What's the biggest work challenge you're facing right now?",
        "Your career is important, but it shouldn't come at the cost of your wellbeing. If work is draining you, it might be time to set boundaries or explore what truly fulfills you. What would your ideal work situation look like?",
        "Workplace challenges can feel inescapable because we spend so much time there. Remember: you are not your job title. Your worth isn't measured by your productivity. What would help you feel more balanced at work?",
    ],
    "study": [
        "Academic pressure can be intense, but remember: your grades don't define your intelligence or your future. Many successful people struggled in school. What's weighing on you most right now?",
        "Studying smart matters more than studying hard. Try the Pomodoro technique: 25 minutes of focused study, 5-minute break. Repeat. And make sure you're sleeping — your brain consolidates learning during rest. You've got this!",
        "It's normal to feel stressed about exams. Here's what helps: Make a study plan so everything feels more manageable. Take regular breaks. Stay hydrated. And remember that one test doesn't determine your whole future. What subject are you working on?",
    ],
    "health": [
        "Health concerns can be scary, and it's okay to feel anxious about them. If you haven't already, please reach out to a healthcare professional for proper guidance. In the meantime, be gentle with yourself. What's going on?",
        "I understand health worries weigh heavily on the mind. While I can't provide medical advice, I can support you emotionally through this. Would you like to talk about how you're feeling about your health situation?",
    ],
    "money": [
        "Financial stress is one of the most common sources of anxiety, and it's completely valid. Remember: your net worth doesn't determine your self-worth. Would you like to talk about what's worrying you? Sometimes breaking it down into smaller steps makes it more manageable.",
        "Money problems feel overwhelming because they touch every part of our lives. But there's always a path forward. Focus on what you can control today — even small steps like tracking expenses or finding one way to save matter. You're not alone in this.",
    ],
    "philosophy": [
        "That's a fascinating question to think about. Philosophers have debated these ideas for thousands of years, and there's beauty in the exploration itself. What draws you to this question?",
        "I love exploring deep questions like this. There may not be a single right answer, but the journey of thinking about it reveals a lot about who we are. What's your own perspective?",
        "These are the kinds of questions that make us truly human. I think the fact that you're asking shows you're someone who thinks deeply about life. Let's explore this together — what's your take?",
    ],
    "creative": [
        "Creativity is such a beautiful way to express yourself and process emotions. Whether it's writing, painting, music, or any other art form, it connects us to our inner world. What kind of creative work inspires you?",
        "I love that you're feeling creative! Art and expression are powerful tools for healing and self-discovery. Even if it's just doodling or writing a few lines, every creative act matters. What are you working on?",
    ],
    "joke": [
        "Here's one for you: Why did the emotion go to therapy? Because it had too many feelings! But seriously, laughter really is good medicine. It releases endorphins and reduces stress hormones. What usually makes YOU laugh?",
        "I wish I could tell you a perfect joke, but here's something that might make you smile: You're talking to an AI about feelings, and that's actually pretty wonderful. The fact that you're checking in with yourself shows real emotional intelligence!",
        "Okay, here's my best one: I tried to write a joke about emotions, but I couldn't find the right tone! Badum-tss. But you know what? The fact that you're here, engaging with your wellbeing, is the real win. What else is on your mind?",
        "Why did the psychology student break up with the biology student? Because they had no chemistry! Here is another: What do you call a fish without eyes? A fsh! Want more?",
    ],
    "comfort": [
        "I wish I could give you a real hug right now, but here's a virtual one: Consider yourself hugged tightly. You are safe here. You are cared for. Whatever you're going through, you don't have to face it alone.",
        "You deserve comfort and warmth. Wrap yourself in something cozy, take a deep breath, and remember: this moment will pass. You are stronger than you know, and you deserve to feel safe and at peace.",
        "Sending you warmth and care. Sometimes we all need a moment of comfort. Take a slow breath in... and let it out. You're doing the best you can, and that's enough.",
    ],
    "crisis": [
        "I'm really concerned about what you just shared, and I want you to know that your life has immense value. Please reach out to a crisis helpline right now — they're trained to help and available 24/7. In the US, call or text 988 (Suicide & Crisis Lifeline). In the UK, call 116 123 (Samaritans). You are not alone, and things can get better. Would you like me to help you find support?",
        "What you're feeling right now is real and painful, but it's not permanent. Please reach out for help immediately — call 988 (US) or 116 123 (UK). These are free, confidential, and available 24/7. Your life matters, and there are people who want to help you through this. You took a brave step by reaching out. Please take the next step and call.",
    ],
}


# ── Practical request responses ────────────────────────────

_SONG_SUGGESTIONS = {
    'sad': [
        'When you are feeling down, try these: Here Comes the Sun by The Beatles, Lean on Me by Bill Withers, or Three Little Birds by Bob Marley. Music has a way of reaching places words cannot.' ,
        'For sad moments, try: Fix You by Coldplay, Someone Like You by Adele, or Bridge Over Troubled Water by Simon and Garfunkel. Let the music hold your feelings.' ,
        'When sadness hits, try: Vienna by Billy Joel, Let It Be by The Beatles, or Happier by Ed Sheeran. Sometimes the right song at the right time changes everything.' ,
    ],
    'anger': [
        'When you are angry, channel it with: Lose Yourself by Eminem, Stronger by Kelly Clarkson, or Fight Song by Rachel Platten. Turn that fire into fuel.' ,
        'For anger, try: Stronger by Kanye West, Shout by Tears for Fears, or Survivor by Destiny Child. Let the music transform your frustration into strength.' ,
        'When you need to release anger through music: In the End by Linkin Park, Born This Way by Lady Gaga, or Break Stuff by Limp Bizkit.' ,
    ],
    'fear': [
        'When you are anxious, try: Weightless by Marconi Union, Clair de Lune by Debussy, or Sunset Lover by Petit Biscuit. Let the music wrap around you.' ,
        'For fear and anxiety, listen to: Breathe Me by Sia, Ocean Eyes by Billie Eilish, or Experience by Ludovico Einaudi.' ,
        'When worry takes over, try: River by Leon Bridges, Holocene by Bon Iver, or No Surprises by Radiohead. These create a safe sonic space.' ,
    ],
    'joy': [
        'When you are happy, celebrate with: Happy by Pharrell Williams, Good as Hell by Lizzo, or Do not Stop Me Now by Queen!' ,
        'For joyful moments: Walking on Sunshine by Katrina and the Waves, Here Comes the Sun by The Beatles, or Best Day of My Life by American Authors.' ,
        'Keep the good vibes going: On Top of the World by Imagine Dragons, Shake It Off by Taylor Swift, or Uptown Funk by Bruno Mars.' ,
    ],
    'calm': [
        'For peaceful moments, try: Clair de Lune by Debussy, Gymnopedie No. 1 by Satie, or Weightless by Marconi Union. Pure tranquility in musical form.' ,
        'When you are feeling calm and want to deepen it: Nuvole Bianche by Ludovico Einaudi, River Flows in You by Yiruma, or Arrival of the Birds by The Cinematic Orchestra.' ,
        'For serenity: Comptine d un autre ete by Yann Tiersen, Merry Christmas Mr. Lawrence by Ryuichi Sakamoto, or Bloom by The Paper Kites.' ,
    ],
    'default': [
        'Here are some great songs: Someone Like You by Adele for reflection, Happy by Pharrell for joy, Weightless by Marconi Union for calm, and Lose Yourself by Eminem for motivation.' ,
        'I would suggest: Here Comes the Sun by The Beatles for hope, River by Leon Bridges for peace, Stronger by Kelly Clarkson for resilience, and Do not Stop Me Now by Queen for energy.' ,
        'Try this mix: Clair de Lune by Debussy for peace, Good as Hell by Lizzo for confidence, Fix You by Coldplay for comfort, and On Top of the World by Imagine Dragons for celebration.' ,
    ],
}

_BOOK_SUGGESTIONS = {
    'default': [
        'Great reads for any mood: The Alchemist by Paulo Coelho for inspiration, Atomic Habits by James Clear for self-improvement, The Power of Now by Eckhart Tolle for peace of mind, or Educated by Tara Westover for an incredible life story.' ,
        'I would recommend: Man Search for Meaning by Viktor Frankl for finding purpose, Big Magic by Elizabeth Gilbert for creativity, or The Midnight Library by Matt Haig for hope.' ,
    ],
}

_MOVIE_SUGGESTIONS = {
    'default': [
        'Great films to watch: Inside Out for understanding emotions, Soul for finding purpose, Good Will Hunting for self-worth, or The Secret Life of Walter Mitty for adventure.' ,
        'I would suggest: A Beautiful Mind for resilience, Soul by Pixar for meaning, The Pursuit of Happyness for inspiration, or Spirited Away for wonder.' ,
    ],
}

_AFFIRMATIONS = [
    'You are enough, exactly as you are. Your worth is not measured by productivity or perfection.' ,
    'You are stronger than you think. Every challenge you have faced has prepared you for what is ahead.' ,
    'You deserve love, peace, and happiness. Do not let anyone, including yourself, tell you otherwise.' ,
    'This moment is temporary. Whatever you are going through will pass, and you will come out stronger.' ,
    'You are not your mistakes. You are the lessons you have learned and the kindness you have chosen to carry forward.' ,
    'It is okay to rest. It is okay to not be okay. You are doing the best you can, and that is always enough.' ,
    'You have survived every bad day you have ever had. Your track record is 100 percent, and that is pretty remarkable.' ,
    'Be gentle with yourself. You are a work in progress, and that is the most beautiful thing to be.' ,
    'The world needs your unique light. Do not dim yourself to make others comfortable. Shine boldly.' ,
    'You are capable of amazing things. Do not let self-doubt silence the voice that knows your potential.' ,
]

_BREATHING_EXERCISES = [
    'Let us try the 4-7-8 technique: Breathe IN through your nose for 4 seconds. HOLD your breath for 7 seconds. Breathe OUT slowly through your mouth for 8 seconds. Repeat 4 times. Feel the tension leaving your body with each exhale.' ,
    'Try box breathing: IN for 4 counts, HOLD for 4 counts, OUT for 4 counts, HOLD for 4 counts. Imagine tracing the sides of a square with your breath. Do this 5 times.' ,
    'Here is a simple one: Place one hand on your chest and one on your belly. Breathe so only the belly hand moves. Breathe in for 4, out for 6. Do this 10 times.' ,
    'Try the physiological sigh: Take a deep breath in through your nose, then take a second shorter breath on top of it. Then exhale slowly through your mouth. This is the fastest way to calm your nervous system. Repeat 3 times.' ,
]

_MEDITATION_GUIDANCE = [
    'Find a comfortable position and close your eyes. Take three deep breaths. Now let your breathing return to normal. Focus only on the sensation of air entering and leaving your nostrils. When your mind wanders, gently bring it back. No judgment. Just breath. Try this for 5 minutes.' ,
    'Sit quietly and close your eyes. Starting from the top of your head, slowly scan down through your body. Notice any tension without trying to fix it. Just acknowledge it. When you reach your toes, take a deep breath and imagine all that tension flowing out.' ,
    'Close your eyes. With each breath, imagine you are breathing in calm and breathing out worry. Picture a peaceful place. Stay there for a few minutes. This place exists inside you and you can return anytime.' ,
]

_TIPS = [
    'Try the 2-minute rule: If something takes less than 2 minutes, do it now. This prevents small tasks from piling up and creating overwhelm.' ,
    'Write down 3 things you are grateful for before bed. It trains your brain to notice the good, even on hard days.' ,
    'When anxious, name 5 things you can see, 4 you can hear, 3 you can touch, 2 you can smell, and 1 you can taste. This grounds you in the present.' ,
    'Move your body for just 10 minutes. A short walk, some stretching, or dancing to one song can shift your entire mood.' ,
    'Drink a glass of water right now. Dehydration affects mood, energy, and focus more than most people realize.' ,
    'Put your phone in another room for 30 minutes. Digital detox, even briefly, can reduce anxiety and improve sleep quality.' ,
    'Practice the 3 Cs: Catch the negative thought, Challenge it with evidence, Change it to something more balanced.' ,
]

# ── Emotion-specific responses (fallback) ──────────────────

_EMOTION_RESPONSES = {
    "joy": [
        "That's wonderful! I'm really happy to hear you're feeling good. What's been bringing you joy lately?",
        "I love hearing positive energy from you! Happiness like this is worth celebrating. What made your day better?",
        "You sound like you're in a great place right now. That's really lovely. Is there something specific making you feel this way?",
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

_GENERIC = [
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

# ── Knowledge base for common topics ──────────────────────

_KNOWLEDGE = {
    "quantum physics": "Quantum physics is the study of the smallest things in the universe — atoms and subatomic particles. The key ideas are: particles can exist in multiple states at once (superposition), they can be connected across distances (entanglement), and observing something changes it (measurement problem). It's counterintuitive because our everyday experience doesn't prepare us for how weird reality gets at tiny scales. Einstein called it 'spooky action at a distance.' Despite being strange, quantum physics powers your phone, computers, and MRI machines.",
    "physics": "Physics is the study of matter, energy, and the fundamental forces of nature. It ranges from the tiniest particles (quantum physics) to the largest structures in the universe (cosmology). The four fundamental forces are gravity, electromagnetism, the strong nuclear force, and the weak nuclear force. Physics helps us understand everything from why the sky is blue to how black holes work. It's the foundation of all other sciences.",
    "math": "Mathematics is the language of patterns, structures, and relationships. It includes arithmetic (numbers), algebra (equations), geometry (shapes), calculus (change), and statistics (data). Math is used everywhere — from engineering and science to art and music. The beautiful thing about math is that its truths are universal and eternal. What aspect of math are you curious about?",
    "cooking": "Cooking is both an art and a science! The basic principles are: heat transfer (how food absorbs energy), chemical reactions (like Maillard browning for flavor), and balancing flavors (salt, sweet, sour, bitter, umami). The most important tip is to taste as you go and season gradually. Good cooking starts with fresh ingredients and simple techniques. Would you like a specific recipe or cooking tip?",
    "pasta": "Making pasta from scratch is easier than you think! Basic recipe: Mix 2 cups flour with 3 large eggs and a pinch of salt. Knead for 10 minutes until smooth, then let it rest for 30 minutes. Roll it thin (by hand or with a machine), cut into your desired shape, and cook in boiling salted water for 2-4 minutes. The key is getting the dough smooth and elastic — if it's too dry, add a tiny bit of water. Fresh pasta tastes incredible with just butter, parmesan, and fresh herbs.",
    "exercise": "Regular exercise is one of the best things you can do for your mental and physical health. For beginners: start with 15-20 minutes of walking daily. Gradually add strength exercises (bodyweight squats, push-ups, planks). Aim for 150 minutes of moderate activity per week. The key is consistency over intensity. Exercise releases endorphins, reduces cortisol, improves sleep, and boosts mood. Find something you enjoy — dancing, swimming, cycling — and it won't feel like a chore.",
    "sleep tips": "Good sleep hygiene includes: keep a consistent sleep schedule (even on weekends), avoid screens 1 hour before bed, keep your room cool (65-68°F/18-20°C), limit caffeine after 2pm, and create a calming bedtime routine. The 4-7-8 breathing technique (inhale 4s, hold 7s, exhale 8s) helps many people fall asleep. If you can't sleep after 20 minutes, get up and do something calming, then return. Avoid napping after 3pm.",
    "nutrition": "Good nutrition is about balance, not perfection. Focus on: plenty of vegetables and fruits, whole grains for sustained energy, lean proteins for muscle and brain health, healthy fats (olive oil, nuts, avocado), and staying hydrated (8 glasses of water daily). The Mediterranean diet is one of the most well-researched healthy eating patterns. Remember — food is fuel AND pleasure. Enjoy what you eat mindfully.",
    "procrastination": "Procrastination is usually about emotion, not time management. We avoid tasks that trigger anxiety, boredom, or perfectionism. The solution: break tasks into tiny steps (2-minute rule), start with the easiest part, set specific deadlines, remove distractions, and reward yourself for starting (not finishing). The Pomodoro Technique works well: 25 minutes of focus, 5-minute break. Be kind to yourself — procrastination is human, not a character flaw.",
    "anxiety": "Anxiety is your brain's alarm system going off, often when there's no real danger. It's very common and very treatable. Short-term tools: deep breathing (4-7-8 technique), grounding (5-4-3-2-1 senses exercise), journaling your worries, and limiting caffeine. Long-term: regular exercise, therapy (especially CBT), mindfulness meditation, and adequate sleep. Remember: anxiety lies to you. You've survived every anxious moment so far. What specifically triggers your anxiety?",
    "depression": "Depression is more than just feeling sad — it's a real medical condition that affects how you think, feel, and function. It's not a weakness or something you can just 'snap out of.' If you're experiencing persistent low mood, loss of interest, changes in sleep/appetite, or difficulty concentrating, please reach out to a healthcare professional. In the meantime: maintain a routine, get sunlight, move your body, stay connected with people, and be incredibly gentle with yourself. You deserve help and support.",
    "meditation": "Meditation is the practice of training your attention and awareness. Here is how to start: sit comfortably, close your eyes, focus on your breath. When your mind wanders (it will), gently bring it back without judgment. Start with just 5 minutes daily. Types include: mindfulness (focus on breath/body), loving-kindness (directing compassion), and body scan (progressive relaxation). The benefits are well-documented: reduced stress, better focus, improved emotional regulation, and even structural brain changes. There is no wrong way to meditate — even trying counts.",
    "yoga": "Yoga combines physical postures, breathing exercises, and meditation for total wellbeing. For beginners: start with Hatha or Yin yoga (gentler styles). Key poses for stress relief: Child's Pose, Cat-Cow, Forward Fold, Legs Up the Wall, and Corpse Pose (Savasana). Even 15 minutes daily makes a difference. Yoga reduces cortisol, improves flexibility, builds strength, and calms the nervous system. You do not need to be flexible to start — flexibility is a result, not a requirement.",
    "time management": "Effective time management starts with knowing your priorities. Try the Eisenhower Matrix: urgent+important (do now), important but not urgent (schedule), urgent but not important (delegate), neither (eliminate). Other tips: batch similar tasks, use time blocks, tackle hard tasks when your energy peaks (usually morning), and build in buffer time. Remember: being busy is not the same as being productive. Rest is productive too.",
    "self-esteem": "Self-esteem is how you value yourself. Low self-esteem often comes from negative self-talk, comparison to others, or past experiences. To build it: challenge negative thoughts (are they actually true?), celebrate small wins, set achievable goals, practice self-compassion, surround yourself with supportive people, and focus on your strengths. You are not defined by your worst moments. Treat yourself the way you would treat a good friend.",
    "productivity": "Real productivity is about working smarter, not harder. Key principles: know your top 3 priorities each day, work in focused blocks (90 minutes max), take regular breaks, eliminate distractions proactively, and say no to non-essential commitments. The best productivity system is the one you actually use. Start simple: pick your most important task and do it first, before checking email or social media. Protect your morning energy.",
    "relationships": "Healthy relationships are built on mutual respect, communication, and boundaries. Key practices: listen to understand (not to respond), express needs clearly, respect differences, apologize genuinely, and maintain your own identity. Red flags include: controlling behavior, constant criticism, gaslighting, and isolation from loved ones. Remember: you cannot change another person, only yourself. A relationship should add to your life, not drain it.",
    "cooking healthy": "Healthy cooking does not have to be complicated. Focus on: more vegetables (aim for half your plate), lean proteins (chicken, fish, beans, tofu), whole grains (brown rice, quinoa, whole wheat), and healthy cooking methods (grilling, steaming, roasting instead of frying). Flavor your food with herbs, spices, citrus, and garlic instead of excess salt. Meal prep on weekends to make weekday cooking easier. The best healthy diet is one you enjoy and can sustain.",
    "travel": "Travel opens your mind to new cultures, perspectives, and experiences. Budget tips: book flights on Tuesdays, travel in shoulder season, stay in hostels or Airbnbs, eat where locals eat, and use public transit. For meaningful travel: slow down (stay longer in fewer places), learn basic phrases in the local language, be curious about local customs, and keep a journal. The best trips are about connection — with people, places, and yourself.",
    "reading": "Reading is one of the best habits for mental health and personal growth. Benefits include: reduced stress (by up to 68%), improved focus, expanded vocabulary, better sleep (when reading physical books), and increased empathy. To build a reading habit: start with books you genuinely enjoy, carry a book everywhere, set a small daily goal (10 pages), and join a book club for accountability. What genre interests you? I can suggest some great reads.",
    "technology": "Technology shapes every aspect of modern life. Key trends right now include: AI and machine learning (like ChatGPT), quantum computing, renewable energy tech, biotechnology, and space exploration. For mental health, technology can be a double-edged sword — it connects us but can also increase anxiety and comparison. Healthy tech habits: set screen time limits, use blue light filters at night, take regular digital detoxes, and be intentional about what you consume online.",
    "space": "Space is incredibly vast and fascinating. Our observable universe is about 93 billion light-years in diameter. Key facts: there are more stars in the universe than grains of sand on Earth, light takes 8 minutes to reach us from the Sun, a day on Venus is longer than its year, and there is a giant cloud of alcohol in space (Sagittarius B2). The nearest star to us (after the Sun) is Proxima Centauri, about 4.24 light-years away. We are all literally made of star stuff — the elements in our bodies were formed in ancient supernovae.",
    "history": "History helps us understand who we are and how we got here. Some pivotal moments: the invention of writing (3400 BC), the fall of Rome (476 AD), the Renaissance (1300s-1600s), the Scientific Revolution, the Industrial Revolution, the World Wars, the Moon landing (1969), and the rise of the internet (1990s). History shows us that humanity has faced enormous challenges before and found ways through. What period or event interests you most?",
    "psychology": "Psychology is the scientific study of the mind and behavior. Key concepts: cognitive biases (systematic errors in thinking), the Big Five personality traits (openness, conscientiousness, extraversion, agreeableness, neuroticism), attachment theory (how early bonds shape relationships), and the fight-or-flight response. Understanding psychology helps you make better decisions, understand others, and navigate emotions. Books like 'Thinking, Fast and Slow' by Daniel Kahneman are great starting points.",
    "philosophy general": "Philosophy explores fundamental questions about existence, knowledge, ethics, and meaning. Key branches: metaphysics (what is real?), epistemology (how do we know things?), ethics (what is right and wrong?), and logic (how do we reason?). Famous philosophers include Socrates (question everything), Aristotle (virtue ethics), Kant (categorical imperative), Nietzsche (will to power), and existentialists like Sartre and Camus. Philosophy is not abstract — it shapes how we live, love, and make choices every day.",
    "economics": "Economics studies how people allocate scarce resources. Key concepts: supply and demand, inflation, GDP, opportunity cost, and market equilibrium. Personal finance basics: live below your means, save 20% of income if possible, invest early (compound interest is powerful), avoid high-interest debt, and build an emergency fund (3-6 months expenses). Understanding economics helps you make better financial decisions and understand the world around you.",
}


def _detect_intent(message):
    """Detect the user's intent from their message."""
    text = message.lower().strip()
    # Remove common filler words for better matching
    words = text.split()

    for intent, config in _INTENT_PATTERNS.items():
        keywords = config["keywords"]
        match_type = config["match"]

        if match_type == "prefix":
            if any(text.startswith(kw) for kw in keywords):
                return intent
        elif match_type == "contains":
            # Direct substring match
            if any(kw in text for kw in keywords):
                return intent
            # For multi-word keywords, check if all words appear (flexible match)
            for kw in keywords:
                kw_words = kw.split()
                if len(kw_words) > 1:
                    if all(w in words for w in kw_words):
                        return intent

    return None


def _get_companion_reply(message):
    """Generate a universal, intelligent companion reply."""
    text = message.strip()
    text_lower = text.lower()

    # 1. Check for crisis first (highest priority)
    if _detect_intent(text) == "crisis":
        return _random.choice(_RESPONSES["crisis"])

    # 2. Check knowledge base for factual/general questions
    for topic, answer in _KNOWLEDGE.items():
        if topic in text_lower:
            return answer

    # Also check for 'how to' / 'how do I' patterns for knowledge
    how_to_patterns = ["how to", "how do i", "how can i", "how do you", "explain", "what is a", "what are", "tell me about", "describe", "define"]
    for pattern in how_to_patterns:
        if pattern in text_lower:
            # Try to find a matching topic in knowledge base
            for topic, answer in _KNOWLEDGE.items():
                topic_words = topic.split()
                if any(w in text_lower for w in topic_words if len(w) > 3):
                    return answer
            # If no topic matches, give a helpful general response
            return _random.choice([
                "That's an interesting question! While I'm primarily a wellness companion, I love exploring different topics with you. Could you tell me more about what you're curious about? I'll share what I know.",
                "Great question! I enjoy thinking about a wide range of topics. Let me share my perspective: every question is worth asking. What specifically about this interests you most?",
                "I appreciate your curiosity! While I'm focused on emotional wellness, I'm happy to explore any topic with you. The fact that you're asking questions shows great intellectual curiosity.",
            ])

    # 3. Check for specific intents that use separate response pools
    intent = _detect_intent(text)

    if intent == "suggest_songs":
        result = analyze_emotion(text)
        emotion = result["emotion"]
        pool = _SONG_SUGGESTIONS.get(emotion, _SONG_SUGGESTIONS.get("default"))
        return _random.choice(pool)

    if intent == "suggest_book":
        pool = _BOOK_SUGGESTIONS.get("default")
        return _random.choice(pool)

    if intent == "suggest_movie":
        pool = _MOVIE_SUGGESTIONS.get("default")
        return _random.choice(pool)

    if intent == "affirmation":
        return _random.choice(_AFFIRMATIONS)

    if intent == "breathing":
        return _random.choice(_BREATHING_EXERCISES)

    if intent == "meditation":
        return _random.choice(_MEDITATION_GUIDANCE)

    if intent == "tip":
        return _random.choice(_TIPS)

    # 4. Check for intents that use _RESPONSES dict
    if intent and intent in _RESPONSES:
        return _random.choice(_RESPONSES[intent])

    # 5. If no specific intent, use emotion detection for fallback
    result = analyze_emotion(text)
    emotion = result["emotion"]

    if emotion in _EMOTION_RESPONSES:
        return _random.choice(_EMOTION_RESPONSES[emotion])

    # 6. Generic fallback
    return _random.choice(_GENERIC)
