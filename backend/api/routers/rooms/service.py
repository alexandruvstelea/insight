from ...database.models.room import Room
from ...database.models.building import Building
from ..buildings.schemas import BuildingOutMinimal
from .schemas import RoomOut, RoomOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def room_to_out(room: Room) -> RoomOut:
    return RoomOut(
        id=room.id,
        name=room.name,
        building_id=room.building_id,
        building=building_to_minimal(room.building),
    )


def building_to_minimal(building: Building) -> BuildingOutMinimal:
    return BuildingOutMinimal(id=building.id, name=building.name)


async def id_to_building(session: AsyncSession, building_id: int) -> Building:
    building = await session.get(Building, building_id)
    if building:
        return building_to_minimal(building)
    raise HTTPException(status_code=404, detail=f"No building with id={building_id}.")
