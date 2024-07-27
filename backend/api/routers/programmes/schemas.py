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


from ..faculties.schemas import FacultyOutMinimal
from ..subjects.schemas import SubjectOutMinimal

ProgrammeOut.model_rebuild()
