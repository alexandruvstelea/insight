from ...database.models.faculty import Faculty
from ...database.models.building import Building
from ..buildings.schemas import BuildingOutMinimal
from .schemas import FacultyOut
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


def faculty_to_out(faculty: Faculty) -> FacultyOut:
    return FacultyOut(
        id=faculty.id,
        name=faculty.name,
        abbreviation=faculty.abbreviation,
        buildings=[building_to_minimal(building) for building in faculty.buildings],
    )


def building_to_minimal(building: Building) -> BuildingOutMinimal:
    return BuildingOutMinimal(id=building.id, name=building.name)


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
