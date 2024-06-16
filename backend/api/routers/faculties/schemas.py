from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class FacultyBase(BaseModel):
    name: str
    abbreviation: str


class FacultyIn(FacultyBase):
    buildings: List[int]
    professors: List[int]


class FacultyOutMinimal(FacultyBase):
    id: int


class FacultyOut(FacultyBase):
    id: int
    buildings: Optional[List["BuildingOutMinimal"]]
    professors: Optional[List["ProfessorOutMinimal"]]


from ..buildings.schemas import BuildingOutMinimal
from ..professors.schemas import ProfessorOutMinimal

FacultyOut.model_rebuild()
