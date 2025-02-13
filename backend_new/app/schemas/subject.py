from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from typing import List, Literal


class SubjectBase(BaseModel):
    name: str
    abbreviation: str
    semester: Literal[1, 2]
    course_professor_id: Optional[int]
    laboratory_professor_id: Optional[int]
    seminar_professor_id: Optional[int]
    project_professor_id: Optional[int]


class SubjectIn(SubjectBase):
    programmes_ids: Optional[List[int]] = []
    sessions_ids: Optional[List[int]] = []


class SubjectOutMinimal(SubjectBase):
    id: int


class SubjectOut(SubjectBase):
    id: int
    programmes: Optional[List["ProgrammeOutMinimal"]] = []
    sessions: Optional[List["SessionOutMinimal"]] = []
    course_professor: Optional["ProfessorOutMinimal"]
    laboratory_professor: Optional["ProfessorOutMinimal"]
    seminar_professor: Optional["ProfessorOutMinimal"]
    project_professor: Optional["ProfessorOutMinimal"]


class SubjectFilter(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    semester: Optional[Literal[1, 2]] = None
    course_professor_id: Optional[int] = None
    laboratory_professor_id: Optional[int] = None
    seminar_professor_id: Optional[int] = None
    project_professor_id: Optional[int] = None
    programme_id: Optional[int] = None
    session_id: Optional[int] = None


from app.schemas.programme import ProgrammeOutMinimal
from app.schemas.session import SessionOutMinimal
from app.schemas.professor import ProfessorOutMinimal

SubjectOut.model_rebuild()
