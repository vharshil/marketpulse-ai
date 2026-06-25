import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [value, setValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (value.trim()) {
      onSearch(value);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-wrapper">
        <span className="search-icon">🔍</span>
        <input
          className="search-input"
          type="text"
          placeholder="Search company... e.g. Tata Motors, Apple"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          autoFocus
        />
        <button className="search-btn" type="submit">
          Analyse
        </button>
      </div>
    </form>
  );
}

export default SearchBar;