from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class BuildingBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class BuildingIn(BuildingBase):
    faculties_ids: Optional[List[int]] = []
    rooms_ids: Optional[List[int]] = []


class BuildingOutMinimal(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class BuildingOut(BuildingBase):
    id: int
    latitude: float
    longitude: float
    rooms: Optional[List["RoomOutMinimal"]]
    faculties: Optional[List["FacultyOutMinimal"]]

    class Config:
        from_attributes = True


class BuildingFilter(BaseModel):
    name: Optional[str] = None
    faculty_id: Optional[int] = None


from app.schemas.room import RoomOutMinimal
from app.schemas.faculty import FacultyOutMinimal

BuildingOut.model_rebuild()
