from ...database.models.faculty import Faculty
from ...database.models.building import Building
from ...database.models.room import Room
from ..faculties.schemas import FacultyOutMinimal
from ..rooms.schemas import RoomOutMinimal
from .schemas import BuildingOut
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select


async def building_to_out(building: Building) -> BuildingOut:
    print(
        BuildingOut(
            id=building.id,
            name=building.name,
            rooms=(
                [room_to_minimal(room) for room in building.rooms]
                if await building.rooms
                else []
            ),
            faculties=[faculty_to_minimal(faculty) for faculty in building.faculties],
        )
    )
    return BuildingOut(
        id=building.id,
        name=building.name,
        rooms=(
            [room_to_minimal(room) for room in building.rooms]
            if await building.rooms
            else []
        ),
        faculties=[faculty_to_minimal(faculty) for faculty in building.faculties],
    )


def room_to_minimal(room: Room) -> RoomOutMinimal:
    return RoomOutMinimal(id=room.id, name=room.name, building_id=room.building_id)


def faculty_to_minimal(faculty: Faculty) -> FacultyOutMinimal:
    return FacultyOutMinimal(
        id=faculty.id, name=faculty.name, abbreviation=faculty.abbreviation
    )


async def ids_to_faculties(
    session: AsyncSession, faculty_ids: List[int]
) -> List[Faculty]:
    result = await session.execute(select(Faculty).where(Faculty.id.in_(faculty_ids)))
    faculties = result.scalars().all()
    if len(faculties) != len(faculty_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more faculties not found for IDs {faculty_ids}",
        )
    return list(faculties)
