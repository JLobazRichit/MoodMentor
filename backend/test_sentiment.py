from transformers import pipeline


print("Loading MoodMentor sentiment model...")


sentiment_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
)


print("MoodMentor sentiment model loaded.")


def analyze_sentiment(text: str):

    result = sentiment_classifier(text)[0]

    return {
        "sentiment": result["label"],
        "score": round(result["score"] * 100, 2),
    }