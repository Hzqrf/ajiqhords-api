from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import engine, get_db
import models
import schemas

# Create tables if not using migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ajiqhords API")

# Setup CORS for the UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Ajiqhords API"}

@app.get("/api/songs/", response_model=List[schemas.SongShortResponse])
def get_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Fetch songs with their total view count
    songs_with_views = db.query(
        models.Song.id,
        models.Song.title,
        models.Song.artist,
        models.Song.genre,
        models.Song.original_key,
        models.Song.difficulty,
        func.count(models.SongView.id).label('views')
    ).outerjoin(models.SongView, models.Song.id == models.SongView.song_id)\
     .group_by(models.Song.id)\
     .offset(skip).limit(limit).all()
    
    return songs_with_views

@app.post("/api/songs/", response_model=schemas.SongResponse)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = models.Song(
        title=song.title,
        artist=", ".join(song.artist),
        genre=song.genre,
        original_key=song.original_key,
        difficulty=song.difficulty,
        content=song.content
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/api/songs/top", response_model=List[schemas.SongShortResponse])
def get_top_songs(period: str = "week", limit: int = 5, db: Session = Depends(get_db)):
    """
    Get top songs based on view count for a specific period: week, month, year, or all.
    """
    query = db.query(
        models.Song.id, 
        models.Song.title, 
        models.Song.artist,
        models.Song.genre,
        models.Song.original_key,
        models.Song.difficulty,
        func.count(models.SongView.id).label('view_count')
    ).join(models.SongView, models.Song.id == models.SongView.song_id)

    # Filter by time period
    now = datetime.utcnow()
    if period == "week":
        start_date = now - timedelta(days=7)
        query = query.filter(models.SongView.viewed_at >= start_date)
    elif period == "month":
        start_date = now - timedelta(days=30)
        query = query.filter(models.SongView.viewed_at >= start_date)
    elif period == "year":
        start_date = now - timedelta(days=365)
        query = query.filter(models.SongView.viewed_at >= start_date)
    
    # Group, sort and limit
    top_songs = query.group_by(models.Song.id).order_by(func.count(models.SongView.id).desc()).limit(limit).all()
    
    # Map results to schema
    result = []
    for s in top_songs:
        result.append({
            "id": s.id,
            "title": s.title,
            "artist": s.artist,
            "genre": s.genre,
            "original_key": s.original_key,
            "difficulty": s.difficulty,
            "views": s.view_count
        })
    
    return result

@app.get("/api/songs/{song_id}", response_model=schemas.MockSongResponse)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Record a new view
    new_view = models.SongView(song_id=song_id)
    db.add(new_view)
    db.commit()
    
    # Get total view count
    total_views = db.query(func.count(models.SongView.id)).filter(models.SongView.song_id == song_id).scalar()
    
    # Add views to the song object for the response
    song.views = total_views
    
    return song

@app.post("/api/requests/", response_model=schemas.SongRequestResponse)
def create_request(request: schemas.SongRequestCreate, db: Session = Depends(get_db)):
    db_request = models.SongRequest(
        title=request.title,
        artist=request.artist,
        notes=request.notes
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
