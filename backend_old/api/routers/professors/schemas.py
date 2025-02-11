from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, Literal


class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    gender: Literal["male", "female"]


class ProfessorIn(ProfessorBase):
    faculties: Optional[List[int]]


class ProfessorOutMinimal(ProfessorBase):
    id: int


class ProfessorOut(ProfessorBase):
    id: int
    faculties: Optional[List["FacultyOutMinimal"]]
    courses: Optional[List["SubjectOutMinimal"]]
    laboratories: Optional[List["SubjectOutMinimal"]]
    seminars: Optional[List["SubjectOutMinimal"]]
    projects: Optional[List["SubjectOutMinimal"]]


from ..faculties.schemas import FacultyOutMinimal
from ..subjects.schemas import SubjectOutMinimal

ProfessorOut.model_rebuild()
