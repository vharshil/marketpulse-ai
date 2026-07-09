from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from news_service import fetch_news
from gemini_service import analyze_sentiment, answer_question
from ml_service import predict_trend, compute_fusion_score
from database import save_search, get_history
from fastapi.responses import Response
from report_service import generate_report_pdf

load_dotenv()

app = FastAPI(
    title="MarketPulse AI Backend",
    description="Stock sentiment + ML trend analysis platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8002",
        "http://localhost:8003",
        "http://localhost:8004",
        "https://marketpulse-ai-seven.vercel.app",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    company: str
    context: str


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "MarketPulse AI Backend v2.0 is running 🚀",
    }


@app.get("/analyze")
async def analyze(company: str):
    if not company or len(company.strip()) < 2:
        raise HTTPException(status_code=400, detail="Company name too short")

    company = company.strip()

    articles = await fetch_news(company)
    if not articles:
        raise HTTPException(status_code=404, detail=f"No news found for {company}")

    sentiment_result = await analyze_sentiment(company, articles)
    ml_result = await predict_trend(company)
    fusion = compute_fusion_score(sentiment_result["sentiment"], ml_result)

    await save_search(
        company=company,
        sentiment=sentiment_result["sentiment"],
        ml_result=ml_result,
        fusion=fusion,
        summary=sentiment_result.get("summary", "")
    )

    return {
        "company": company,
        "articles_count": len(articles),
        "articles": articles,
        "sentiment": sentiment_result["sentiment"],
        "summary": sentiment_result.get("summary", ""),
        "chart_data": sentiment_result["chart_data"],
        "ml_prediction": ml_result,
        "fusion_score": fusion,
    }


@app.post("/chat")
async def chat(body: ChatRequest):
    answer = await answer_question(
        question=body.question,
        company=body.company,
        context=body.context
    )
    return {"answer": answer}


@app.get("/history")
async def history():
    """Returns the last 10 searches from the database."""
    records = await get_history(limit=10)
    return {"history": records}
@app.get("/report")
async def generate_report(company: str):
    """
    Generates and returns a PDF research report for a company.
    The frontend triggers a file download when this is called.
    """
    if not company or len(company.strip()) < 2:
        raise HTTPException(status_code=400, detail="Company name too short")

    company = company.strip()

    articles = await fetch_news(company)
    if not articles:
        raise HTTPException(status_code=404, detail=f"No news found for {company}")

    sentiment_result = await analyze_sentiment(company, articles)
    ml_result = await predict_trend(company)
    fusion = compute_fusion_score(sentiment_result["sentiment"], ml_result)

    ai_analysis = await answer_question(
        question=f"Give a detailed 3-4 paragraph investment research analysis of {company} based on the current news sentiment and market conditions.",
        company=company,
        context=sentiment_result.get("summary", "")
    )

    pdf_bytes = generate_report_pdf(
        company=company,
        sentiment=sentiment_result["sentiment"],
        ml_prediction=ml_result,
        fusion_score=fusion,
        articles=articles,
        summary=sentiment_result.get("summary", ""),
        ai_analysis=ai_analysis,
    )

    filename = f"MarketPulse_{company.replace(' ', '_')}_Report.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/news")
async def get_news(company: str):
    articles = await fetch_news(company)
    return {
        "company": company,
        "articles_count": len(articles),
        "articles": articles
    }