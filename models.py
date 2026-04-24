from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    artist = Column(String(255), index=True)
    genre = Column(String(100), index=True)
    original_key = Column(String(10))
    difficulty = Column(String(50))
    content = Column(Text)

class SongView(Base):
    __tablename__ = "song_views"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id", ondelete="CASCADE"), nullable=False)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())

class SongRequest(Base):
    __tablename__ = "song_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    notes = Column(Text)
    status = Column(String(50), server_default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
