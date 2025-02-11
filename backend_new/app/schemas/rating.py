from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional, Literal


class RatingBase(BaseModel):
    rating_clarity: int
    rating_interactivity: int
    rating_relevance: int
    rating_comprehension: int
    timestamp: datetime
    session_type: Literal["course", "laboratory", "project", "seminar"]


class RatingIn(BaseModel):
    rating_clarity: int
    rating_interactivity: int
    rating_relevance: int
    rating_comprehension: int
    timestamp: datetime
    programme_id: int
    room_code: str
    latitude: float
    longitude: float


class RatingOut(RatingBase):
    id: int
    rating_overall: float
    subject_id: int
    programme_id: int
    professor_id: int
    faculty_id: int
    room_id: int


class RatingAverageOut(BaseModel):
    rating_overall_average: float
    rating_clarity_average: float
    rating_interactivity_average: float
    rating_relevance_average: float
    rating_comprehension_average: float


class WeekRatings(BaseModel):
    clarity: Optional[float] = None
    interactivity: Optional[float] = None
    relevance: Optional[float] = None
    comprehension: Optional[float] = None
    overall: Optional[float] = None


class RatingFilter(BaseModel):
    timestamp_after: Optional[datetime] = None
    timestamp_before: Optional[datetime] = None
    session_type: Optional[Literal["course", "laboratory", "project", "seminar"]] = None
    subject_id: Optional[int] = None
    programme_id: Optional[int] = None
    professor_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room_id: Optional[int] = None


class GraphDataRatings(BaseModel):
    week_ratings: Dict[str, WeekRatings]
