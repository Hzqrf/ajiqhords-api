from pydantic import BaseModel, Field, field_validator
from typing import List, Union, Optional

class SongCreate(BaseModel):
    title: str
    artist: List[str]
    genre: Optional[str] = None
    original_key: Optional[str] = None
    difficulty: Optional[str] = None
    content: str

class SongBase(BaseModel):
    title: str
    artist: List[str]
    genre: Optional[str] = None
    original_key: Optional[str] = None
    difficulty: Optional[str] = None

    @field_validator('artist', mode='before')
    @classmethod
    def split_artist(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [a.strip() for a in v.split(',')]
        return v

    class Config:
        from_attributes = True

class SongShortResponse(SongBase):
    id: int
    views: Optional[int] = 0

class MockSongResponse(SongBase):
    content: str
    views: Optional[int] = 0

class SongResponse(MockSongResponse):
    id: int

class SongRequestCreate(BaseModel):
    title: str
    artist: str
    notes: Optional[str] = None

class SongRequestResponse(BaseModel):
    id: int
    title: str
    artist: str
    notes: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
