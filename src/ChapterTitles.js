import React from 'react';
import './ChapterTitles.css';

const ChapterTitles = ({ chapters, onReadChapter, loading, selectedChapterIndex }) => {
  if (!chapters || chapters.length === 0) {
    return null;
  }

  return (
    <div className="chapter-titles-section">
      <div className="section-header">
        <h2>Chapter Outline</h2>
        <span className="chapter-count">{chapters.length} chapters</span>
      </div>
      
      <div className="chapters-list">
        {chapters.map((chapter, index) => (
          <div key={index} className="chapter-item">
            <div className="chapter-number-badge">
              Chapter {index + 1}
            </div>
            
            <div className="chapter-content">
              <h3 className="chapter-title">
                {chapter["Chapter Title"]}
              </h3>
              <p className="chapter-description">
                {chapter["Chapter Description"]}
              </p>
            </div>
            
            <div className="chapter-action">
              <button 
                onClick={() => onReadChapter(index)}
                disabled={loading && selectedChapterIndex === index}
                className="read-chapter-btn"
              >
                {loading && selectedChapterIndex === index ? (
                  <>
                    <span className="spinner"></span>
                    Loading...
                  </>
                ) : (
                  <>
                    📚 Read Chapter
                  </>
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="helper-text">
        <p>Click "Read Chapter" to generate and view the full content of any chapter</p>
      </div>
    </div>
  );
};

export default ChapterTitles;
