from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


class ProgrammeBase(BaseModel):
    name: str
    abbreviation: str
    type: int


class ProgrammeIn(ProgrammeBase):
    faculty_id: int
    subjects: List["SubjectOutMinimal"]


class ProgrammeOutMinimal(ProgrammeBase):
    id: int


class ProgrammeOut(ProgrammeBase):
    id: int
    faculty: Optional["FacultyOutMinimal"]
    subjects: Optional[List["SubjectOutMinimal"]]


from ..faculties.schemas import FacultyOutMinimal
from ..subjects.schemas import SubjectOutMinimal

ProgrammeOut.model_rebuild()
