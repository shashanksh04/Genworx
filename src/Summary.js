import React from 'react';
import './Summary.css';

const Summary = ({ summary, onGenerateChapters, loading }) => {
  if (!summary) {
    return null;
  }

  // Calculate word count
  const wordCount = summary.trim().split(/\s+/).length;

  return (
    <div className="summary-section">
      <div className="section-header">
        <h2>Story Summary</h2>
        <span className="word-count">{wordCount} words</span>
      </div>
      
      <div className="summary-container">
        <div className="summary-icon">📖</div>
        <div className="summary-content">
          <p className="summary-text">{summary}</p>
        </div>
      </div>

      <div className="action-section">
        <button 
          onClick={onGenerateChapters} 
          disabled={loading}
          className="next-step-btn"
        >
          {loading ? "Generating Chapters..." : "Generate Chapter Titles"}
        </button>
      </div>
    </div>
  );
};

export default Summary;
