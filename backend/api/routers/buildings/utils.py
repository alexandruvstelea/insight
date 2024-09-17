from ...database.models.building import Building
from ..rooms.utils import room_to_minimal
from .schemas import BuildingOut, BuildingOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


async def building_to_out(building: Building) -> BuildingOut | None:
    from ..faculties.utils import faculty_to_minimal
    if building:
        logger.info(f"Converting building {building.name} to BuildingOut format.")
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
    return None


def building_to_minimal(building: Building) -> BuildingOutMinimal:
    if building:
        logger.info(f"Converting building {building.name} to BuildingOutMinimal format.")
        return BuildingOutMinimal(id=building.id, name=building.name)
    return None

async def id_to_building(session: AsyncSession, building_id: int) -> Building:
    try:
        if building_id:
            logger.info(f"Retrieving building for ID {building_id}.")
            building = await session.get(Building, building_id)
            if building:
                logger.info(f"Retrieved building with ID {building_id}.")
                return building
            logger.error(f"No building with ID {building_id}.")
            raise HTTPException(
                status_code=404, detail=f"No building with ID {building_id}."
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving building with ID {building_id}:\n{e}"
        )
        raise e


async def ids_to_buildings(
    session: AsyncSession, building_ids: List[int]
) -> List[Building]:
    try:
        if building_ids:
            logger.info(f"Retrieving buildings with IDs {building_ids}.")
            result = await session.execute(
                select(Building).where(Building.id.in_(building_ids))
            )
            buildings = result.scalars().all()
            if len(buildings) != len(building_ids):
                logger.error(f"One or more buildings not found for IDs {building_ids}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"One or more buildings not found for IDs {building_ids}",
                )
            logger.info(f"Retrieved buildings with IDs {building_ids}.")
            return list(buildings)
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving buildings with IDs {building_ids}:\n{e}"
        )
        raise e
