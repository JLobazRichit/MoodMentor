from gemini_recommender import generate_recommendation


result = generate_recommendation(
    text="I am stressed because I have an exam tomorrow and I haven't finished studying.",
    emotion="fear",
    emotion_score=82.5,
    sentiment="NEGATIVE",
    sentiment_score=94.2,
)

print()
print("===================================")
print("MOODMENTOR AI RECOMMENDATION")
print("===================================")
print()
print(result)
print()