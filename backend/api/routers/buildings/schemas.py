from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class BuildingBase(BaseModel):
    name: str


class BuildingIn(BuildingBase):
    faculties: List[int]

    class Config:
        from_attributes = True


class BuildingOutMinimal(BuildingBase):
    id: int


class BuildingOut(BuildingBase):
    id: int
    faculties: Optional[List["FacultyOutMinimal"]]


from ..faculties.schemas import FacultyOutMinimal

BuildingOut.model_rebuild()
