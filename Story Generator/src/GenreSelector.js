import React from 'react';
import './GenreSelector.css';

const GenreSelector = ({ genre, setGenre, onGenerate, loading }) => {
  const genreList = [
    "Thriller", 
    "Romance", 
    "Crime",
    "Comedy",
    "Action",
    "Adventure",
    "Science Fiction",
    "Fantasy",
    "Horror",
    "Drama",
    "Young Adult"
  ];

  return (
    <div className="genre-selector">
      <h2>Select a Genre</h2>
      <div className="selector-container">
        <select 
          value={genre} 
          onChange={(e) => setGenre(e.target.value)}
          disabled={loading}
          className="genre-dropdown"
        >
          <option value="">-- Choose a genre --</option>
          {genreList.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
        
        <button 
          onClick={onGenerate} 
          disabled={!genre || loading}
          className="generate-btn"
        >
          {loading ? "Generating Characters..." : "Generate Characters"}
        </button>
      </div>
      
      {!genre && (
        <p className="helper-text">Please select a genre to start generating your story</p>
      )}
    </div>
  );
};

export default GenreSelector;
