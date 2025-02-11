from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


class RoomBase(BaseModel):
    name: str


class RoomIn(RoomBase):
    building_id: int
    unique_code: Optional[str]
    sessions: Optional[List[int]]


class RoomOutMinimal(RoomBase):
    id: int


class RoomOut(RoomBase):
    id: int
    unique_code: str
    building: Optional["BuildingOutMinimal"]
    sessions: Optional[List["SessionOutMinimal"]]


from ..buildings.schemas import BuildingOutMinimal
from ..sessions.schemas import SessionOutMinimal

RoomOut.model_rebuild()
