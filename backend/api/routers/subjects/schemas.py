from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from typing import List


class SubjectBase(BaseModel):
    name: str
    abbreviation: str
    semester: int
    course_professor_id: Optional[int]
    laboratory_professor_id: Optional[int]
    seminar_professor_id: Optional[int]
    project_professor_id: Optional[int]


class SubjectIn(SubjectBase):
    programmes: Optional[List[int]]


class SubjectOutMinimal(SubjectBase):
    id: int


class SubjectOut(SubjectBase):
    id: int
    programmes: Optional[List["ProgrammeOutMinimal"]]


from ..programmes.schemas import ProgrammeOutMinimal

SubjectOut.model_rebuild()
