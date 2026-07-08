

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase connected")
    except Exception as e:
        print(f"⚠️ Supabase connection failed: {e}")


async def save_search(company: str, sentiment: dict, ml_result: dict, fusion: dict, summary: str):
    """Saves a completed search to the database."""
    if not supabase_client:
        print("No database connected — skipping save")
        return

    try:
        data = {
            "company": company,
            "verdict": sentiment.get("verdict", "Neutral"),
            "bullish": sentiment.get("bullish", 0),
            "bearish": sentiment.get("bearish", 0),
            "neutral": sentiment.get("neutral", 0),
            "ml_prediction": ml_result.get("prediction", "N/A") if ml_result.get("available") else "N/A",
            "fusion_signal": fusion.get("signal", "N/A"),
            "summary": summary[:300] if summary else "",
        }
        supabase_client.table("searches").insert(data).execute()
        print(f"✅ Saved search: {company}")
    except Exception as e:
        print(f"⚠️ DB save error: {e}")


async def get_history(limit: int = 10) -> list:
    """Returns the most recent searches from the database."""
    if not supabase_client:
        return []

    try:
        response = (
            supabase_client
            .table("searches")
            .select("company, verdict, bullish, bearish, neutral, ml_prediction, fusion_signal, searched_at")
            .order("searched_at", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data or []
    except Exception as e:
        print(f"⚠️ DB read error: {e}")
        return []