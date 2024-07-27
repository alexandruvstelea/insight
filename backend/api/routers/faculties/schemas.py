from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class FacultyBase(BaseModel):
    name: str
    abbreviation: str


class FacultyIn(FacultyBase):
    buildings: Optional[List[int]]
    professors: Optional[List[int]]
    programmes: Optional[List[int]]


class FacultyOutMinimal(FacultyBase):
    id: int


class FacultyOut(FacultyBase):
    id: int
    buildings: Optional[List["BuildingOutMinimal"]]
    professors: Optional[List["ProfessorOutMinimal"]]
    programmes: Optional[List["ProgrammeOutMinimal"]]


from ..buildings.schemas import BuildingOutMinimal
from ..professors.schemas import ProfessorOutMinimal
from ..programmes.schemas import ProgrammeOutMinimal

FacultyOut.model_rebuild()
