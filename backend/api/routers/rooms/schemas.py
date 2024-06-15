from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class RoomBase(BaseModel):
    name: str


class RoomIn(RoomBase):
    building_id: int


class RoomOutMinimal(RoomBase):
    id: int


class RoomOut(RoomBase):
    id: int
    building: Optional["BuildingOutMinimal"]


from ..buildings.schemas import BuildingOutMinimal

RoomOut.model_rebuild()
