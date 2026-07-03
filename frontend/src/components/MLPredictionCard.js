import React from 'react';
import './MLPredictionCard.css';

function MLPredictionCard({ mlPrediction, fusionScore }) {
  if (!mlPrediction) return null;

  if (!mlPrediction.available) {
    return (
      <div className="ml-card ml-unavailable">
        <div className="ml-header">
          <span className="ml-icon">🤖</span>
          <div>
            <h3 className="ml-title">ML Trend Prediction</h3>
            <p className="ml-subtitle">RandomForest Model</p>
          </div>
        </div>
        <p className="ml-unavailable-msg">{mlPrediction.reason}</p>
      </div>
    );
  }

  const predictionColor = {
    Up: 'var(--accent-green)',
    Down: 'var(--accent-red)',
    Sideways: 'var(--accent-yellow)',
  }[mlPrediction.prediction] || 'var(--accent-blue)';

  const predictionEmoji = {
    Up: '📈',
    Down: '📉',
    Sideways: '➡️',
  }[mlPrediction.prediction] || '📊';

  const fusionColor = {
    Bullish: 'var(--accent-green)',
    Bearish: 'var(--accent-red)',
    Neutral: 'var(--accent-yellow)',
    Mixed: 'var(--accent-yellow)',
  }[fusionScore?.signal] || 'var(--accent-blue)';

  const agreementColor = fusionScore?.agreement === 'Conflicting'
    ? 'var(--accent-red)'
    : 'var(--accent-green)';

  return (
    <div className="ml-card">

      <div className="ml-header">
        <span className="ml-icon">🤖</span>
        <div>
          <h3 className="ml-title">ML Trend Prediction</h3>
          <p className="ml-subtitle">
            RandomForest · {mlPrediction.data_points} days training data · Ticker: {mlPrediction.ticker}
          </p>
        </div>
      </div>

      <div className="ml-body">

        <div className="ml-prediction-row">
          <div className="ml-prediction-main">
            <span className="ml-pred-emoji">{predictionEmoji}</span>
            <span className="ml-pred-text" style={{ color: predictionColor }}>
              {mlPrediction.prediction}
            </span>
          </div>
          <div className="ml-stats">
            <div className="ml-stat">
              <span className="ml-stat-label">Confidence</span>
              <span className="ml-stat-value">{mlPrediction.confidence}%</span>
            </div>
            <div className="ml-stat">
              <span className="ml-stat-label">Model Accuracy</span>
              <span className="ml-stat-value">{mlPrediction.model_accuracy}%</span>
            </div>
            <div className="ml-stat">
              <span className="ml-stat-label">Current Price</span>
              <span className="ml-stat-value">₹{mlPrediction.current_price}</span>
            </div>
            <div className="ml-stat">
              <span className="ml-stat-label">1D Change</span>
              <span
                className="ml-stat-value"
                style={{ color: mlPrediction.price_change_1d >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}
              >
                {mlPrediction.price_change_1d >= 0 ? '+' : ''}{mlPrediction.price_change_1d}%
              </span>
            </div>
          </div>
        </div>

        <div className="ml-probs">
          {Object.entries(mlPrediction.probabilities).map(([label, prob]) => {
            const color = label === 'Up'
              ? 'var(--accent-green)'
              : label === 'Down'
              ? 'var(--accent-red)'
              : 'var(--accent-yellow)';
            return (
              <div key={label} className="ml-prob-row">
                <span className="ml-prob-label">{label}</span>
                <div className="ml-prob-bar">
                  <div
                    className="ml-prob-fill"
                    style={{ width: `${prob}%`, background: color }}
                  />
                </div>
                <span className="ml-prob-val">{prob}%</span>
              </div>
            );
          })}
        </div>

        {fusionScore && (
          <div className="fusion-box">
            <div className="fusion-header">
              <span className="fusion-label">⚡ Fusion Confidence Score</span>
              <span
                className="fusion-agreement"
                style={{ color: agreementColor }}
              >
                {fusionScore.agreement}
              </span>
            </div>
            <div className="fusion-score-row">
              <span
                className="fusion-signal"
                style={{ color: fusionColor }}
              >
                {fusionScore.signal}
              </span>
              <span className="fusion-level">{fusionScore.confidence_level} Confidence</span>
            </div>
            <p className="fusion-explanation">{fusionScore.explanation}</p>
            <div className="fusion-bar">
              <div
                className="fusion-bar-fill"
                style={{
                  width: `${fusionScore.score}%`,
                  background: fusionColor
                }}
              />
            </div>
            <p className="ml-disclaimer">{mlPrediction.disclaimer}</p>
          </div>
        )}

      </div>
    </div>
  );
}

export default MLPredictionCard;