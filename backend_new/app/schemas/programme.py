from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, Literal


class ProgrammeBase(BaseModel):
    name: str
    abbreviation: str
    type: Literal["bachelor", "master", "phd"]


class ProgrammeIn(ProgrammeBase):
    faculty_id: int
    subjects: Optional[List[int]]


class ProgrammeOutMinimal(ProgrammeBase):
    id: int


class ProgrammeOut(ProgrammeBase):
    id: int
    faculty: Optional["FacultyOutMinimal"]
    subjects: Optional[List["SubjectOutMinimal"]]


class ProgrammeFilter(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    type: Optional[Literal["bachelor", "master", "phd"]] = None
    faculty_id: Optional[int] = None
    subject_id: Optional[int] = None


from app.schemas.faculty import FacultyOutMinimal
from app.schemas.subject import SubjectOutMinimal

ProgrammeOut.model_rebuild()
