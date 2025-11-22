import React from 'react';
import './ChapterContent.css';

const ChapterContent = ({ 
  chapterContent, 
  chapterTitle, 
  chapterIndex, 
  onClose,
  onDownload 
}) => {
  if (!chapterContent) {
    return null;
  }

  // Calculate word count
  const wordCount = chapterContent.trim().split(/\s+/).length;

  // Download chapter as text file
  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([chapterContent], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `Chapter_${chapterIndex + 1}_${chapterTitle.replace(/[^a-z0-9]/gi, '_')}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="chapter-content-overlay">
      <div className="chapter-content-modal">
        <div className="modal-header">
          <div className="header-info">
            <span className="chapter-label">Chapter {chapterIndex + 1}</span>
            <h2 className="modal-title">{chapterTitle}</h2>
          </div>
          <button onClick={onClose} className="close-btn" aria-label="Close">
            ✕
          </button>
        </div>

        <div className="modal-meta">
          <span className="word-count-badge">📊 {wordCount} words</span>
          <button onClick={handleDownload} className="download-btn">
            💾 Download Chapter
          </button>
        </div>

        <div className="modal-body">
          <div className="chapter-text">
            {chapterContent}
          </div>
        </div>

        <div className="modal-footer">
          <button onClick={onClose} className="close-footer-btn">
            Close Chapter
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChapterContent;
