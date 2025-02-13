from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class FacultyBase(BaseModel):
    name: str
    abbreviation: str


class FacultyIn(FacultyBase):
    buildings_ids: Optional[List[int]] = []
    professors_ids: Optional[List[int]] = []
    programmes_ids: Optional[List[int]] = []


class FacultyOutMinimal(FacultyBase):
    id: int

    class Config:
        from_attributes = True


class FacultyOut(FacultyBase):
    id: int
    buildings: Optional[List["BuildingOutMinimal"]] = []
    professors: Optional[List["ProfessorOutMinimal"]] = []
    programmes: Optional[List["ProgrammeOutMinimal"]] = []

    class Config:
        from_attributes = True


class FacultyFilter(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    building_id: Optional[int] = None
    professor_id: Optional[int] = None
    progamme_id: Optional[int] = None


from app.schemas.building import BuildingOutMinimal
from app.schemas.professor import ProfessorOutMinimal
from app.schemas.programme import ProgrammeOutMinimal

FacultyOut.model_rebuild()
