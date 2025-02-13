from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, Literal


class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    gender: Literal["male", "female"]


class ProfessorIn(ProfessorBase):
    faculties_ids: Optional[List[int]] = []


class ProfessorOutMinimal(ProfessorBase):
    id: int

    class Config:
        from_attributes = True


class ProfessorOut(ProfessorBase):
    id: int
    faculties: Optional[List["FacultyOutMinimal"]] = []
    courses: Optional[List["SubjectOutMinimal"]] = []
    laboratories: Optional[List["SubjectOutMinimal"]] = []
    seminars: Optional[List["SubjectOutMinimal"]] = []
    projects: Optional[List["SubjectOutMinimal"]] = []

    class Config:
        from_attributes = True


class ProfessorFilter(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[Literal["male", "female"]] = None
    faculty_id: Optional[int] = None
    course_id: Optional[int] = None
    laboratory_id: Optional[int] = None
    seminar_id: Optional[int] = None
    project_id: Optional[int] = None


from app.schemas.faculty import FacultyOutMinimal
from app.schemas.subject import SubjectOutMinimal

ProfessorOut.model_rebuild()
