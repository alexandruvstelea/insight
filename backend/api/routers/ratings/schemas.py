from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class RatingBase(BaseModel):
    rating_clarity: int
    rating_interactivity: int
    rating_relevance: int
    rating_comprehension: int
    timestamp: datetime
    session_type: str


class RatingIn(RatingBase):
    programme_id: int
    room_id: int


class RatingOut(RatingBase):
    id: int
    rating_overall: float
    subject_id: int
    programme_id: int
    professor_id: int
    faculty_id: int
    room_id: int
