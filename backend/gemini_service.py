from google import genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


async def analyze_sentiment(company: str, articles: list) -> dict:
    if not client:
        return _mock_sentiment(articles)

    headlines = "\n".join([
        f"- [{a['source']}] {a['title']}"
        for a in articles[:10]
    ])

    prompt = f"""You are a financial news sentiment analyst for Indian stock markets.

Analyse these recent news headlines about "{company}":

{headlines}

Return ONLY a valid JSON object. No markdown, no explanation, just raw JSON:
{{
  "sentiment": {{
    "bullish": <integer 0-100>,
    "bearish": <integer 0-100>,
    "neutral": <integer 0-100>,
    "verdict": "<Bullish or Bearish or Neutral>",
    "score": <integer 0-100>
  }},
  "chart_data": [
    {{"name": "Bullish", "value": <integer>}},
    {{"name": "Bearish", "value": <integer>}},
    {{"name": "Neutral", "value": <integer>}}
  ],
  "summary": "<2-3 sentences summarising the overall market mood for a retail investor>",
  "per_article_sentiment": [<list of Bullish or Bearish or Neutral for each headline in order>]
}}

Rules:
- bullish + bearish + neutral must add up to exactly 100
- verdict must match whichever of the three is highest
- per_article_sentiment must have exactly the same count as the headlines above"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        raw = response.text.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        result = json.loads(raw)

        per_article = result.get("per_article_sentiment", [])
        for i, article in enumerate(articles):
            article["sentiment"] = per_article[i] if i < len(per_article) else "Neutral"

        return result

    except Exception as e:
        print(f"Gemini error: {e}")
        return _mock_sentiment(articles)


async def answer_question(question: str, company: str, context: str) -> str:
    if not client:
        return f"Based on recent news, {company} shows mixed signals. Add Gemini key for real answers."

    prompt = f"""You are a helpful stock research assistant for Indian retail investors.

The user is asking about "{company}".

News context from today:
{context}

User question: {question}

Answer in 2-3 sentences. Be clear and helpful.
Always end with: "Note: This is based on news sentiment only, not financial advice." """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print(f"Gemini chat error: {e}")
        return "I am having trouble connecting to AI right now. Please try again."


def _mock_sentiment(articles: list) -> dict:
    sentiments = ["Bullish", "Bearish", "Bullish", "Neutral", "Bullish"]
    for i, article in enumerate(articles):
        article["sentiment"] = sentiments[i % len(sentiments)]

    return {
        "sentiment": {
            "bullish": 55,
            "bearish": 25,
            "neutral": 20,
            "verdict": "Bullish",
            "score": 55,
        },
        "chart_data": [
            {"name": "Bullish", "value": 55},
            {"name": "Bearish", "value": 25},
            {"name": "Neutral", "value": 20},
        ],
        "summary": "Recent news shows a generally positive outlook with product launches and expansion plans. Some caution remains due to global market uncertainty.",
        "per_article_sentiment": sentiments,
    }