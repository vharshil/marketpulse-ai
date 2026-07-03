

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


def get_stock_ticker(company: str) -> str:
    """
    Maps company names to their stock ticker symbols.
    yfinance needs tickers not company names.
    Indian stocks need .NS suffix for NSE listing.
    """
    ticker_map = {
        "tata motors": "TATAMOTORS.NS",
        "reliance": "RELIANCE.NS",
        "infosys": "INFY.NS",
        "hdfc bank": "HDFCBANK.NS",
        "zomato": "ZOMATO.NS",
        "wipro": "WIPRO.NS",
        "tcs": "TCS.NS",
        "apple": "AAPL",
        "tesla": "TSLA",
        "google": "GOOGL",
        "microsoft": "MSFT",
        "amazon": "AMZN",
    }
    return ticker_map.get(company.lower().strip(), None)


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    RSI = Relative Strength Index
    Measures momentum — is the stock overbought or oversold?
    RSI > 70 = overbought (price may fall)
    RSI < 30 = oversold (price may rise)
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates technical indicator features from raw OHLCV data.
    These are the same indicators professional traders use.

    Features we create:
    - MA5, MA20: 5-day and 20-day moving averages
    - MA_ratio: short MA / long MA (>1 means uptrend)
    - RSI: momentum indicator
    - Volume_ratio: current volume vs 20-day average
    - Daily_return: % price change from yesterday
    - Volatility: 5-day rolling standard deviation
    """
    df = df.copy()

    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA_ratio'] = df['MA5'] / df['MA20']

    df['RSI'] = calculate_rsi(df['Close'])

    df['Volume_ratio'] = df['Volume'] / df['Volume'].rolling(window=20).mean()

    df['Daily_return'] = df['Close'].pct_change()

    df['Volatility'] = df['Daily_return'].rolling(window=5).std()

    df['Target'] = np.where(
        df['Close'].shift(-1) > df['Close'] * 1.005, 'Up',
        np.where(df['Close'].shift(-1) < df['Close'] * 0.995, 'Down', 'Sideways')
    )

    return df


async def predict_trend(company: str) -> dict:
    """
    Main function — downloads data, trains model, returns prediction.
    Called from main.py as part of the /analyze endpoint.
    """
    ticker = get_stock_ticker(company)

    if not ticker:
        return _unknown_stock_result(company)

    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False)

        if df.empty or len(df) < 50:
            return _insufficient_data_result(company)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = prepare_features(df)
        df = df.dropna()

        if len(df) < 30:
            return _insufficient_data_result(company)

        feature_cols = ['MA_ratio', 'RSI', 'Volume_ratio', 'Daily_return', 'Volatility']
        X = df[feature_cols].values
        y = df['Target'].values

        split = int(len(X) * 0.8)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        le = LabelEncoder()
        y_train_enc = le.fit_transform(y_train)
        y_test_enc = le.transform(y_test)

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=5
        )
        model.fit(X_train, y_train_enc)

        accuracy = model.score(X_test, y_test_enc)

        last_features = X[-1].reshape(1, -1)
        prediction_enc = model.predict(last_features)[0]
        probabilities = model.predict_proba(last_features)[0]
        prediction = le.inverse_transform([prediction_enc])[0]

        confidence = float(max(probabilities) * 100)

        classes = le.classes_
        prob_dict = {}
        for cls, prob in zip(classes, probabilities):
            prob_dict[cls] = round(float(prob) * 100, 1)

        current_price = float(df['Close'].iloc[-1])
        price_change = float(df['Daily_return'].iloc[-1] * 100)

        return {
            "available": True,
            "ticker": ticker,
            "prediction": prediction,
            "confidence": round(confidence, 1),
            "probabilities": prob_dict,
            "model_accuracy": round(accuracy * 100, 1),
            "current_price": round(current_price, 2),
            "price_change_1d": round(price_change, 2),
            "data_points": len(df),
            "disclaimer": "ML prediction based on historical patterns only. Not financial advice."
        }

    except Exception as e:
        print(f"ML prediction error for {company}: {e}")
        return _error_result(company)


def compute_fusion_score(sentiment: dict, ml_result: dict) -> dict:
    """
    THE UNIQUE FEATURE — combines GenAI sentiment + ML trend into one signal.

    Logic:
    - If both agree (bullish sentiment + Up trend) = HIGH confidence
    - If they disagree (bullish sentiment + Down trend) = LOW confidence, flag as mixed
    - If ML not available = use sentiment only

    This conflict detection is what makes MarketPulse AI different from
    any basic sentiment app. Mention this in interviews!
    """
    if not ml_result.get("available"):
        return {
            "score": sentiment.get("score", 50),
            "signal": sentiment.get("verdict", "Neutral"),
            "confidence_level": "Medium",
            "agreement": "N/A",
            "explanation": "Based on news sentiment only. ML data not available for this stock."
        }

    verdict = sentiment.get("verdict", "Neutral")
    ml_pred = ml_result.get("prediction", "Sideways")
    ml_conf = ml_result.get("confidence", 50)
    sent_score = sentiment.get("score", 50)

    bullish_signals = (
        (verdict == "Bullish" and ml_pred == "Up") or
        (verdict == "Bullish" and ml_pred == "Sideways") or
        (verdict == "Neutral" and ml_pred == "Up")
    )

    bearish_signals = (
        (verdict == "Bearish" and ml_pred == "Down") or
        (verdict == "Bearish" and ml_pred == "Sideways") or
        (verdict == "Neutral" and ml_pred == "Down")
    )

    disagreement = (
        (verdict == "Bullish" and ml_pred == "Down") or
        (verdict == "Bearish" and ml_pred == "Up")
    )

    if disagreement:
        fusion_score = 50
        signal = "Mixed"
        confidence_level = "Low"
        agreement = "Conflicting"
        explanation = (
            f"News sentiment is {verdict} but ML model predicts {ml_pred} price trend. "
            f"Conflicting signals detected — proceed with caution."
        )
    elif bullish_signals:
        fusion_score = min(95, int((sent_score + ml_conf) / 2) + 10)
        signal = "Bullish"
        confidence_level = "High" if fusion_score > 70 else "Medium"
        agreement = "Aligned"
        explanation = (
            f"Both news sentiment ({verdict}) and ML price trend ({ml_pred}) "
            f"point in the same positive direction. Strong bullish signal."
        )
    elif bearish_signals:
        fusion_score = max(5, int((sent_score + ml_conf) / 2) - 10)
        signal = "Bearish"
        confidence_level = "High" if fusion_score < 30 else "Medium"
        agreement = "Aligned"
        explanation = (
            f"Both news sentiment ({verdict}) and ML price trend ({ml_pred}) "
            f"point in the same negative direction. Strong bearish signal."
        )
    else:
        fusion_score = 50
        signal = "Neutral"
        confidence_level = "Low"
        agreement = "Neutral"
        explanation = "Mixed or neutral signals from both news and price trend analysis."

    return {
        "score": fusion_score,
        "signal": signal,
        "confidence_level": confidence_level,
        "agreement": agreement,
        "explanation": explanation
    }


def _unknown_stock_result(company: str) -> dict:
    return {
        "available": False,
        "reason": f"Ticker not found for '{company}'. Supported: Tata Motors, Reliance, Infosys, HDFC Bank, Zomato, Apple, Tesla, Google, Microsoft, Amazon.",
    }


def _insufficient_data_result(company: str) -> dict:
    return {
        "available": False,
        "reason": f"Insufficient historical data for '{company}'.",
    }


def _error_result(company: str) -> dict:
    return {
        "available": False,
        "reason": f"Could not run ML analysis for '{company}' right now.",
    }