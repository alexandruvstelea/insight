from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class FacultyBase(BaseModel):
    name: str
    abbreviation: str


class FacultyIn(FacultyBase):
    buildings: List[int]

    class Config:
        from_attributes = True


class FacultyOutMinimal(FacultyBase):
    id: int


class FacultyOut(FacultyBase):
    id: int
    buildings: Optional[List["BuildingOutMinimal"]]


from ..buildings.schemas import BuildingOutMinimal

FacultyOut.model_rebuild()
