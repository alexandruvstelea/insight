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
    programmes: Optional[List[int]]
    sessions: Optional[List[int]]


class SubjectOutMinimal(SubjectBase):
    id: int


class SubjectOut(SubjectBase):
    id: int
    programmes: Optional[List["ProgrammeOutMinimal"]]
    sessions: Optional[List["SessionOutMinimal"]]
    course_professor: Optional["ProfessorOutMinimal"]
    laboratory_professor: Optional["ProfessorOutMinimal"]
    seminar_professor: Optional["ProfessorOutMinimal"]
    project_professor: Optional["ProfessorOutMinimal"]


from ..programmes.schemas import ProgrammeOutMinimal
from ..sessions.schemas import SessionOutMinimal
from ..professors.schemas import ProfessorOutMinimal

SubjectOut.model_rebuild()
