from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from app.backend import (
    generate_characters,
    generate_summary,
    generate_chapter_titles,
    generate_chapter_content,
)

app = FastAPI()

# Enable CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schemas
class GenreRequest(BaseModel):
    genre: str

class SummaryRequest(BaseModel):
    genre: str
    characters: List[Dict[str, str]]

class ChaptersRequest(BaseModel):
    characters: List[Dict[str, str]]
    summary: str

class ChapterContentRequest(BaseModel):
    genre: str
    characters: List[Dict[str, str]]
    summary: str
    chapter: Dict[str, Any]



@app.post("/characters/")
async def characters_endpoint(request: GenreRequest):
    chars = generate_characters(request.genre)
    return chars


@app.post("/summary/")
async def summary_endpoint(request: SummaryRequest):
    summary = generate_summary(request.genre, request.characters)
    return {"summary": summary}


@app.post("/chapters/")
async def chapters_endpoint(request: ChaptersRequest):
    chapters = generate_chapter_titles(request.characters, request.summary)
    return chapters


@app.post("/chapter_content/")
async def chapter_content_endpoint(request: ChapterContentRequest):
    content = generate_chapter_content(
        request.genre, request.characters, request.summary, request.chapter
    )
    return {"content": content}
