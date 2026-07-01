import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import SentimentCards from '../components/SentimentCards';
import SentimentChart from '../components/SentimentChart';
import NewsFeed from '../components/NewsFeed';
import AIChatBox from '../components/AIChatBox';
import { analyzeStock } from '../services/api';
import './HomePage.css';

function HomePage() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searched, setSearched] = useState('');

  const handleSearch = async (company) => {
    setIsLoading(true);
    setError(null);
    setResults(null);
    setSearched(company);
    try {
      const data = await analyzeStock(company);
      setResults(data);
    } catch (err) {
      setError('Something went wrong. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <p className="hero-eyebrow">India's smartest stock research platform</p>
          <h1 className="hero-title">
            Research smarter,{' '}
            <span className="hero-highlight">invest better</span>
          </h1>
          <p className="hero-subtitle">
            Type any NSE, BSE or global stock. MarketPulse AI reads
            live news, scores sentiment with Gemini AI, and gives you
            a full research report in seconds.
          </p>
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
          <div className="hero-examples">
            <p className="examples-label">Try searching:</p>
            <div className="example-chips">
              {['Reliance', 'Tata Motors', 'Infosys', 'HDFC Bank', 'Zomato'].map((name) => (
                <button
                  key={name}
                  className="chip"
                  onClick={() => handleSearch(name)}
                  disabled={isLoading}
                >
                  {name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {isLoading && (
        <section className="results-section">
          <div className="loading-state">
            <div className="loading-spinner" />
            <p className="loading-text">Fetching live news for "{searched}"...</p>
            <p className="loading-sub">Running Gemini AI analysis</p>
          </div>
        </section>
      )}

      {error && (
        <section className="results-section">
          <div className="error-box">
            <span>⚠️</span>
            <p>{error}</p>
          </div>
        </section>
      )}

      {results && !isLoading && (
        <section className="results-section">
          <div className="results-header">
            <h2 className="results-title">
              Sentiment Analysis —{' '}
              <span className="results-company">{results.company}</span>
            </h2>
            <p className="results-meta">
              Based on {results.articles_count} live articles · Just now
            </p>
          </div>
          <SentimentCards sentiment={results.sentiment} />
          <div className="two-col-grid">
            <SentimentChart data={results.chart_data} />
            <NewsFeed articles={results.articles} />
          </div>
          <AIChatBox
            company={results.company}
            context={results.summary}
          />
        </section>
      )}

      {!results && !isLoading && !error && (
        <section className="empty-state">
          <p className="empty-hint">
            Search any company above to see live AI sentiment analysis
          </p>
        </section>
      )}
    </div>
  );
}

export default HomePage;