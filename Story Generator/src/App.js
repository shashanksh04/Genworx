import React, { useState } from 'react';
import './App.css';
import GenreSelector from './GenreSelector';
import CharacterList from './CharacterList';
import Summary from './Summary';
import ChapterTitles from './ChapterTitles';
import ChapterContent from './ChapterContent';

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

function App() {
  // State management
  const [genre, setGenre] = useState("");
  const [characters, setCharacters] = useState([]);
  const [summary, setSummary] = useState("");
  const [chapters, setChapters] = useState([]);
  const [selectedChapterIndex, setSelectedChapterIndex] = useState(null);
  const [chapterContent, setChapterContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  // API base URL
  const API_BASE = "http://localhost:8000";

  // Generate Characters
  const generateCharacters = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/characters/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ genre }),
      });
      const data = await res.json();
      setCharacters(data);
      setCurrentStep(1);
    } catch (error) {
      console.error("Error generating characters:", error);
      alert("Failed to generate characters");
    }
    setLoading(false);
  };

  // Generate Summary
  const generateSummary = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/summary/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ genre, characters }),
      });
      const data = await res.json();
      setSummary(data.summary);
      setCurrentStep(2);
    } catch (error) {
      console.error("Error generating summary:", error);
      alert("Failed to generate summary");
    }
    setLoading(false);
  };

  // Generate Chapter Titles
  const generateChapters = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/chapters/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ characters, summary }),
      });
      const data = await res.json();
      setChapters(data);
      setCurrentStep(3);
    } catch (error) {
      console.error("Error generating chapters:", error);
      alert("Failed to generate chapters");
    }
    setLoading(false);
  };

  // Generate Chapter Content
  const generateChapterContent = async (chapterIndex) => {
    setLoading(true);
    setSelectedChapterIndex(chapterIndex);
    try {
      const chapter = chapters[chapterIndex];
      const res = await fetch(`${API_BASE}/chapter_content/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          genre, 
          characters, 
          summary, 
          chapter 
        }),
      });
      const data = await res.json();
      setChapterContent(data.content);
    } catch (error) {
      console.error("Error generating chapter content:", error);
      alert("Failed to generate chapter content");
    }
    setLoading(false);
  };

  // Reset all data
  const resetAll = () => {
    setGenre("");
    setCharacters([]);
    setSummary("");
    setChapters([]);
    setSelectedChapterIndex(null);
    setChapterContent("");
    setCurrentStep(0);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎭 AI Story Generator</h1>
        <p>Generate complete stories using local LLMs</p>
      </header>

      <div className="container">
        {/* Genre Selection */}
        <section className="section">
          <h2>Step 1: Select Genre</h2>
          <GenreSelector 
            genre={genre}
            setGenre={setGenre}
            onGenerate={generateCharacters}
            loading={loading && currentStep === 0}
          />
          {/* <select 
            value={genre} 
            onChange={(e) => setGenre(e.target.value)}
            disabled={loading}
            className="genre-select"
          >
            <option value="">Choose a genre...</option>
            {genreList.map(g => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select> */}
          <button 
            onClick={generateCharacters} 
            disabled={!genre || loading}
            className="btn btn-primary"
          >
            {loading && currentStep === 0 ? "Generating..." : "Generate Characters"}
          </button>
        </section>

        {/* Characters Display */}
        {characters.length > 0 && (
          <section className="section">
            <h2>Step 2: Characters ({characters.length})</h2>
            <CharacterList 
              characters={characters}
              onGenerateSummary={generateSummary}
              loading={loading && currentStep === 1}
            />
            {/* <div className="characters-grid">
              {characters.map((c, idx) => (
                <div key={idx} className="character-card">
                  <h3>{c["Character Name"]}</h3>
                  <p>{c["Character Description"]}</p>
                </div>
              ))}
            </div> */}
            <button 
              onClick={generateSummary} 
              disabled={loading}
              className="btn btn-primary"
            >
              {loading && currentStep === 1 ? "Generating..." : "Generate Summary"}
            </button>
          </section>
        )}

        {/* Summary Display */}
        {summary && (
          <section className="section">
            <h2>Step 3: Story Summary</h2>
            <Summary 
              summary={summary}
              onGenerateChapters={generateChapters}
              loading={loading && currentStep === 2}
            />
            <button 
              onClick={generateChapters} 
              disabled={loading}
              className="btn btn-primary"
            >
              {loading && currentStep === 2 ? "Generating..." : "Generate Chapters"}
            </button>
          </section>
        )}

        {/* Chapters Display */}
        {chapters.length > 0 && (
          <section className="section">
            <h2>Step 4: Chapters ({chapters.length})</h2>
            <ChapterTitles 
              chapters={chapters}
              onReadChapter={generateChapterContent}
              loading={loading}
              selectedChapterIndex={selectedChapterIndex}
            />
            <div className="chapters-list">
              {chapters.map((ch, idx) => (
                <div key={idx} className="chapter-item">
                  <div className="chapter-info">
                    <h3>Chapter {idx + 1}: {ch["Chapter Title"]}</h3>
                    <p>{ch["Chapter Description"]}</p>
                  </div>
                  <button 
                    onClick={() => generateChapterContent(idx)}
                    disabled={loading}
                    className="btn btn-secondary"
                  >
                    {loading && selectedChapterIndex === idx ? "Loading..." : "Read Chapter"}
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Chapter Content Display */}
        <ChapterContent 
          chapterContent={chapterContent}
          chapterTitle={selectedChapterIndex !== null ? chapters[selectedChapterIndex]["Chapter Title"] : ""}
          chapterIndex={selectedChapterIndex}
          onClose={() => {
            setChapterContent("");
            setSelectedChapterIndex(null);
          }}
        />
        {chapterContent && (
          <section className="section">
            <h2>Chapter {selectedChapterIndex + 1}: {chapters[selectedChapterIndex]["Chapter Title"]}</h2>
            <div className="chapter-content">
              <p style={{ whiteSpace: 'pre-wrap' }}>{chapterContent}</p>
            </div>
            <button 
              onClick={() => {
                setChapterContent("");
                setSelectedChapterIndex(null);
              }}
              className="btn btn-secondary"
            >
              Close Chapter
            </button>
          </section>
        )}

        {/* Reset Button */}
        {currentStep > 0 && (
          <button onClick={resetAll} className="btn btn-danger">
            Start Over
          </button>
        )}
      </div>
    </div>
  );
}

export default App;
