from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class BuildingBase(BaseModel):
    name: str


class BuildingIn(BuildingBase):
    faculties: List[int]


class BuildingOutMinimal(BuildingBase):
    id: int


class BuildingOut(BuildingBase):
    id: int
    rooms: Optional[List["RoomOutMinimal"]]
    faculties: Optional[List["FacultyOutMinimal"]]


from ..rooms.schemas import RoomOutMinimal
from ..faculties.schemas import FacultyOutMinimal

BuildingOut.model_rebuild()
