from transformers import pipeline


print("Loading MoodMentor emotion model...")

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)

print("MoodMentor emotion model loaded.")


def analyze_emotion(text: str):
    results = emotion_classifier(text)

    # The pipeline returns a list containing
    # the scores for all emotion labels.
    emotions = results[0]

    # Highest-scoring emotion
    best_emotion = max(
        emotions,
        key=lambda item: item["score"]
    )

    return {
        "emotion": best_emotion["label"],
        "score": round(best_emotion["score"] * 100, 2),
        "all_emotions": [
            {
                "label": item["label"],
                "score": round(item["score"] * 100, 2),
            }
            for item in emotions
        ],
    }