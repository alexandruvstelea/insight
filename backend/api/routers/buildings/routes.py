from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import BuildingIn, BuildingOut
from sqlalchemy.ext.asyncio import AsyncSession
from .service import BuildingsService
from http import HTTPStatus
from typing import List

buildings_router = APIRouter(prefix="/api/buildings")


@buildings_router.get("/", response_model=List[BuildingOut], status_code=HTTPStatus.OK)
async def get_buildings(
    session: AsyncSession = Depends(get_session),
) -> List[BuildingOut]:
    buildings = await BuildingsService(session).get_buildings()
    return buildings


@buildings_router.get("/{id}", response_model=BuildingOut, status_code=HTTPStatus.OK)
async def get_building_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    building = await BuildingsService(session).get_building_by_id(id)
    return building


@buildings_router.post("/", response_model=BuildingOut, status_code=HTTPStatus.CREATED)
async def add_building(
    building_data: BuildingIn, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    response = await BuildingsService(session).add_building(building_data)
    return response


@buildings_router.put("/{id}", response_model=BuildingOut, status_code=HTTPStatus.OK)
async def update_building(
    id: int, new_building_data: BuildingIn, session: AsyncSession = Depends(get_session)
) -> BuildingOut:
    response = await BuildingsService(session).update_building(id, new_building_data)
    return response


@buildings_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_building(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await BuildingsService(session).delete_building(id)
    return response
