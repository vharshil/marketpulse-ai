import React, { useEffect, useState } from 'react';
import './SearchHistory.css';

const BACKEND_URL = 'http://localhost:8000';

function SearchHistory({ onSelect }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_URL}/history`)
      .then((res) => res.json())
      .then((data) => {
        setHistory(data.history || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const verdictColor = {
    Bullish: 'var(--accent-green)',
    Bearish: 'var(--accent-red)',
    Neutral: 'var(--accent-yellow)',
  };

  if (loading) return null;
  if (history.length === 0) return null;

  return (
    <div className="history-section">
      <p className="history-label">Recent Searches</p>
      <div className="history-chips">
        {history.map((item, i) => (
          <button
            key={i}
            className="history-chip"
            onClick={() => onSelect(item.company)}
          >
            <span className="history-company">{item.company}</span>
            <span
              className="history-verdict"
              style={{ color: verdictColor[item.verdict] || 'var(--text-muted)' }}
            >
              {item.verdict}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default SearchHistory;