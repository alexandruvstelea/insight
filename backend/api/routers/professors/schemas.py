from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    gender: int


class ProfessorIn(ProfessorBase):
    faculties: List[int]


class ProfessorOutMinimal(ProfessorBase):
    id: int


class ProfessorOut(ProfessorBase):
    id: int
    faculties: Optional[List["FacultyOutMinimal"]]


from ..faculties.schemas import FacultyOutMinimal

ProfessorOut.model_rebuild()
