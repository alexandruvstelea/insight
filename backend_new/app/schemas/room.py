from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


class RoomBase(BaseModel):
    name: str


class RoomIn(RoomBase):
    building_id: int
    unique_code: Optional[str]
    sessions_ids: Optional[List[int]] = []


class RoomOutMinimal(RoomBase):
    id: int

    class Config:
        from_attributes = True


class RoomOut(RoomBase):
    id: int
    unique_code: str
    building: Optional["BuildingOutMinimal"]
    sessions: Optional[List["SessionOutMinimal"]] = []

    class Config:
        from_attributes = True


class RoomFilter(BaseModel):
    name: Optional[str] = None
    unique_code: Optional[str] = None
    session_id: Optional[int] = None


from app.schemas.building import BuildingOutMinimal
from app.schemas.session import SessionOutMinimal

RoomOut.model_rebuild()
