from ...database.models.building import Building
from ..rooms.utils import room_to_minimal
from .schemas import BuildingOut, BuildingOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


async def building_to_out(building: Building) -> BuildingOut:
    from ..faculties.utils import faculty_to_minimal

    return BuildingOut(
        id=building.id,
        name=building.name,
        rooms=(
            [room_to_minimal(room) for room in building.rooms] if building.rooms else []
        ),
        faculties=(
            [faculty_to_minimal(faculty) for faculty in building.faculties]
            if building.faculties
            else []
        ),
    )


def building_to_minimal(building: Building) -> BuildingOutMinimal:
    return BuildingOutMinimal(id=building.id, name=building.name)


async def id_to_building(session: AsyncSession, building_id: int) -> Building:
    building = await session.get(Building, building_id)
    if building:
        return building
    raise HTTPException(status_code=404, detail=f"No building with id={building_id}.")


async def ids_to_buildings(
    session: AsyncSession, building_ids: List[int]
) -> List[Building]:
    result = await session.execute(
        select(Building).where(Building.id.in_(building_ids))
    )
    buildings = result.scalars().all()
    if len(buildings) != len(building_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more buildings not found for IDs {building_ids}",
        )
    return list(buildings)
