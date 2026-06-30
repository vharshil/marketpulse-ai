

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MarketPulse AI Backend",
    description="Backend API for stock sentiment and trend analysis",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Health check endpoint - visit this in browser to confirm server works"""
    return {"status": "ok", "message": "MarketPulse AI Backend is running 🚀"}