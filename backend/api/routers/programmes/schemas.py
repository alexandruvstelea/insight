from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class ProgrammeBase(BaseModel):
    name: str
    abbreviation: str
    type: int


class ProgrammeIn(ProgrammeBase):
    faculty_id: int


class ProgrammeOutMinimal(ProgrammeBase):
    id: int


class ProgrammeOut(ProgrammeBase):
    id: int
    faculty: Optional["FacultyOutMinimal"]


from ..faculties.schemas import FacultyOutMinimal

ProgrammeOut.model_rebuild()
