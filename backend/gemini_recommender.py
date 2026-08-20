import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key:
    client = genai.Client(api_key=api_key)


def generate_recommendation(
    text: str,
    emotion: str,
    emotion_score: float,
    sentiment: str,
    sentiment_score: float,
):
    prompt = f"""
You are MoodMentor, an empathetic AI emotional wellness assistant.

Analyze the user's emotional situation and provide personalized,
practical and supportive recommendations.

User message:
{text}

Detected emotion:
{emotion}

Emotion confidence:
{emotion_score:.1f}%

Detected sentiment:
{sentiment}

Sentiment confidence:
{sentiment_score:.1f}%

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "empathetic_response": "A short supportive response to the user's situation.",
    "recommendations": [
        "First personalized recommendation",
        "Second personalized recommendation",
        "Third personalized recommendation"
    ],
    "wellness_activity": {{
        "title": "Name of the wellness activity",
        "duration": "10 minutes",
        "description": "Short description of how to do the activity."
    }}
}}

Rules:
- Do not use Markdown.
- Do not use bold formatting.
- Do not use numbered lists.
- Do not use bullet symbols.
- Keep the empathetic response under 3 sentences.
- Give exactly 3 personalized recommendations.
- Recommendations must relate specifically to the user's message.
- The wellness activity must match the user's situation and emotion.
- Be supportive and non-judgmental.
- Do not diagnose mental health conditions.
- Do not provide medical diagnosis or treatment.
- Return JSON only.
"""

    if not client:
        return {
            "empathetic_response": "Thank you for sharing how you're feeling. I'm here to listen.",
            "recommendations": [
                "Take a few deep breaths to help calm your mind.",
                "Write down what's on your mind in a journal.",
                "Consider talking to someone you trust about your feelings."
            ],
            "wellness_activity": {
                "title": "Mindful breathing",
                "duration": "5 minutes",
                "description": "Focus on your breath for a few minutes to center yourself."
            }
        }

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    response_text = response.text.strip()

    # Remove accidental Markdown code fences if Gemini adds them
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        recommendation_data = json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "empathetic_response": response_text,
            "recommendations": [],
            "wellness_activity": {
                "title": "Take a short break",
                "duration": "5 minutes",
                "description": (
                    "Take a few slow breaths and give yourself "
                    "a moment to reset."
                ),
            },
        }

    return recommendation_data