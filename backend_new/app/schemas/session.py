from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import time


class SessionBase(BaseModel):
    type: Literal["course", "laboratory", "project", "seminar"]
    semester: Literal[1, 2]
    week_type: Literal[0, 1, 2]
    start: time
    end: time
    day: Literal[0, 1, 2, 3, 4, 5, 6]


class SessionIn(BaseModel):
    type: Literal["course", "laboratory", "project", "seminar"]
    week_type: Literal[0, 1, 2]
    start: time
    end: time
    day: Literal[0, 1, 2, 3, 4, 5, 6]
    room_id: int
    subject_id: int
    faculty_id: int


class SessionOutMinimal(SessionBase):
    id: int

    class Config:
        from_attributes = True


class SessionOut(SessionBase):
    id: int
    room: Optional["RoomOutMinimal"]
    subject: Optional["SubjectOutMinimal"]
    faculty_ids: Optional[List[int]] = []

    class Config:
        from_attributes = True


class SessionFilter(BaseModel):
    type: Optional[Literal["course", "laboratory", "project", "seminar"]] = None
    semester: Optional[Literal[1, 2]] = None
    week_type: Optional[Literal[0, 1, 2]] = None
    start: Optional[time] = None
    end: Optional[time] = None
    day: Optional[Literal[0, 1, 2, 3, 4, 5, 6]] = None
    room_id: Optional[int] = None
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None


from app.schemas.room import RoomOutMinimal
from app.schemas.subject import SubjectOutMinimal

SessionOut.model_rebuild()
