from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import BuildingIn, BuildingOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import BuildingsOperations
from http import HTTPStatus
from typing import List

buildings_router = APIRouter(prefix="/api/buildings")


@buildings_router.get("/", response_model=List[BuildingOut], status_code=HTTPStatus.OK)
async def get_buildings(
    faculty_id: int = None,
    session: AsyncSession = Depends(get_session),
) -> List[BuildingOut]:
    buildings = await BuildingsOperations(session).get_buildings(faculty_id)
    return buildings


@buildings_router.get("/{id}", response_model=BuildingOut, status_code=HTTPStatus.OK)
async def get_building_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    building = await BuildingsOperations(session).get_building_by_id(id)
    return building


@buildings_router.post("/", response_model=BuildingOut, status_code=HTTPStatus.CREATED)
async def add_building(
    building_data: BuildingIn, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    response = await BuildingsOperations(session).add_building(building_data)
    return response


@buildings_router.put("/{id}", response_model=BuildingOut, status_code=HTTPStatus.OK)
async def update_building(
    id: int, new_building_data: BuildingIn, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    response = await BuildingsOperations(session).update_building(id, new_building_data)
    return response


@buildings_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_building(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await BuildingsOperations(session).delete_building(id)
    return response
