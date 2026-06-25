import React, { useState } from 'react';
import SearchBar from '../components/SearchBar';
import './HomePage.css';

function HomePage() {
  const [, setQuery] = useState('');

  const handleSearch = (company) => {
    setQuery(company);
    console.log('Searching for:', company);
  };

  return (
    <div className="home-page">

      <section className="hero-section">
        <div className="hero-content">

          <p className="hero-eyebrow">Powered by Gemini AI + Live News</p>

          <h1 className="hero-title">
            Know what the{' '}
            <span className="hero-highlight">market feels</span>
            <br />
            before you decide
          </h1>

          <p className="hero-subtitle">
            Type any company name. We fetch live news and AI tells
            you if sentiment is Bullish, Bearish or Neutral in seconds.
          </p>

          <SearchBar onSearch={handleSearch} />

          <div className="hero-examples">
            <p className="examples-label">Try searching:</p>
            <div className="example-chips">
              {['Reliance', 'Tata Motors', 'Apple', 'Tesla', 'Infosys'].map((name) => (
                <button
                  key={name}
                  className="chip"
                  onClick={() => handleSearch(name)}
                >
                  {name}
                </button>
              ))}
            </div>
          </div>

        </div>
      </section>

    </div>
  );
}

export default HomePage;