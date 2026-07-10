# 📊 MarketPulse AI — Smart Stock Research Platform

> India's smartest AI-powered stock research platform for retail investors

🌐 **Live Demo:** [marketpulse-ai-seven.vercel.app](https://marketpulse-ai-seven.vercel.app)
💻 **GitHub:** [github.com/vharshil/marketpulse-ai](https://github.com/vharshil/marketpulse-ai)

---

## 🚀 What it does

Search any NSE, BSE or global stock → MarketPulse AI instantly:

1. Fetches **10 live news headlines** from NewsAPI
2. Uses **Google Gemini AI** to score sentiment as Bullish / Bearish / Neutral
3. Runs a **RandomForest ML model** trained on 1 year of historical price data to predict trend direction (Up / Down / Sideways)
4. Combines both signals into a **Fusion Confidence Score** — flags conflicting signals automatically
5. Generates a downloadable **AI Research Report PDF** with full analysis
6. Saves search history to **PostgreSQL (Supabase)** and shows past searches
7. **AI Chat Box** powered by Gemini — ask anything about any stock in natural language

---

## ✨ Features

| Feature | Technology |
|---|---|
| Live news fetching | NewsAPI |
| AI sentiment analysis | Google Gemini 2.0 Flash |
| ML trend prediction | scikit-learn RandomForest |
| Fusion confidence score | Custom algorithm |
| PDF research report | ReportLab + Gemini |
| Search history | PostgreSQL via Supabase |
| AI chat Q&A | Google Gemini API |
| Frontend | React.js, Recharts, CSS Variables |
| Backend | Python, FastAPI |
| Deployment | Vercel + Render |

---

## 🛠️ Tech Stack

**Frontend:** React 18, Recharts, CSS Variables, custom dark theme

**Backend:** Python 3, FastAPI, async endpoints

**AI/ML:**
- Google Gemini 2.0 Flash API for sentiment + chat
- scikit-learn RandomForest classifier
- yfinance for historical OHLCV data
- Features: RSI, Moving Averages (5/20 day), Volume ratio, Daily return, Volatility

**Database:** PostgreSQL hosted on Supabase (free tier)

**Deployment:** Vercel (frontend) + Render (backend)

---

## 📁 Project Structure
marketpulse-ai/
├── frontend/
│   └── src/
│       ├── components/     # Navbar, SearchBar, SentimentCards,
│       │                   # SentimentChart, NewsFeed, AIChatBox,
│       │                   # MLPredictionCard, SearchHistory
│       ├── pages/          # HomePage
│       └── services/       # api.js — all backend calls
└── backend/
├── main.py             # FastAPI server + all endpoints
├── news_service.py     # NewsAPI integration
├── gemini_service.py   # Gemini AI sentiment + chat
├── ml_service.py       # RandomForest model + Fusion Score
├── database.py         # Supabase PostgreSQL
└── report_service.py   # PDF generation with ReportLab
---

## 🚦 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/analyze?company=X` | Full analysis — news + AI + ML + fusion |
| POST | `/chat` | AI chat Q&A about any stock |
| GET | `/history` | Last 10 searches from database |
| GET | `/report?company=X` | Download PDF research report |
| GET | `/news?company=X` | Raw news articles only |

---

## ⚙️ Run Locally

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Create `backend/.env`:
NEWS_API_KEY=your_key
GEMINI_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 🌐 Deployment

- **Frontend** deployed on [Vercel](https://vercel.com) — auto-deploys on every git push
- **Backend** deployed on [Render](https://render.com) — free tier, spins up in ~50s after inactivity
- **Database** hosted on [Supabase](https://supabase.com) — free PostgreSQL

---

## ⚠️ Disclaimer

MarketPulse AI analyses news sentiment and historical price patterns only. It is **NOT financial advice**. Always consult a SEBI-registered investment advisor before making investment decisions.

---

## 👤 Built by

**Harshil Vora** — [LinkedIn](https://linkedin.com/in/harshilvora29) · [GitHub](https://github.com/vharshil)
