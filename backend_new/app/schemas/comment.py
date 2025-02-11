from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class CommentBase(BaseModel):
    text: str
    timestamp: datetime
    session_type: Literal["course", "laboratory", "project", "seminar"]


class CommentIn(BaseModel):
    text: str
    timestamp: datetime
    room_code: str
    programme_id: int
    latitude: float
    longitude: float


class CommentOut(CommentBase):
    id: int
    room_id: int
    programme_id: int
    subject_id: int
    professor_id: int
    faculty_id: int


class CommentFilter(BaseModel):
    timestamp_after: Optional[datetime] = None
    timestamp_before: Optional[datetime] = None
    session_type: Optional[Literal["course", "laboratory", "project", "seminar"]] = None

    class Config:
        from_attributes = True
