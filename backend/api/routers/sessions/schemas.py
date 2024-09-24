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


class SessionOut(SessionBase):
    id: int
    room: Optional["RoomOutMinimal"]
    subject: Optional["SubjectOutMinimal"]
    faculty_id: Optional[List[int]]

from ..rooms.schemas import RoomOutMinimal
from ..subjects.schemas import SubjectOutMinimal

SessionOut.model_rebuild()
