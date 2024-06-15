from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional


class RoomBase(BaseModel):
    name: str
    building_id: int


class RoomIn(RoomBase):
    building_id: Optional[int]

    class Config:
        from_attributes = True


class RoomOutMinimal(RoomBase):
    id: int


class RoomOut(RoomBase):
    id: int
    building: Optional["BuildingOutMinimal"]


from ..buildings.schemas import BuildingOutMinimal

RoomOut.model_rebuild()
