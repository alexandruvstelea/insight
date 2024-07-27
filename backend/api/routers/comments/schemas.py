from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional


class CommentBase(BaseModel):
    text: str
    timestamp: datetime


class CommentIn(CommentBase):
    room_id: int
    programme_id: int


class CommentOut(CommentBase):
    id: int
    room_id: int
    programme_id: int
    subject_id: int
    professor_id: int
    faculty_id: int
