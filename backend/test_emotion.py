from emotion_model import analyze_emotion


text = "I am feeling stressed because of my exams."

result = analyze_emotion(text)

print()
print("========== MOODMENTOR AI ==========")
print("Text:", text)
print("Emotion:", result["emotion"])
print("Confidence:", result["score"], "%")
print()
print("All emotions:")

for emotion in result["all_emotions"]:
    print(
        emotion["label"],
        "→",
        emotion["score"],
        "%"
    )