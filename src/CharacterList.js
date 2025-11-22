import React from 'react';
import './CharacterList.css';

const CharacterList = ({ characters, onGenerateSummary, loading }) => {
  if (!characters || characters.length === 0) {
    return null;
  }

  return (
    <div className="character-list">
      <div className="section-header">
        <h2>Generated Characters</h2>
        <span className="character-count">{characters.length} characters</span>
      </div>
      
      <div className="characters-grid">
        {characters.map((character, index) => (
          <div key={index} className="character-card">
            <div className="character-number">{index + 1}</div>
            <h3 className="character-name">{character["Character Name"]}</h3>
            <p className="character-description">{character["Character Description"]}</p>
          </div>
        ))}
      </div>

      <div className="action-section">
        <button 
          onClick={onGenerateSummary} 
          disabled={loading}
          className="next-step-btn"
        >
          {loading ? "Generating Summary..." : "Generate Story Summary"}
        </button>
      </div>
    </div>
  );
};

export default CharacterList;
