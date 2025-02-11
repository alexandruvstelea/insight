from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.building import BuildingIn, BuildingOut, BuildingFilter
from app.services.implementations.building_service import BuildingService
from app.core.database import get_session
from typing import Optional
from app.core.logging import logger

building_router = APIRouter(prefix="/building", tags=["building"])


@building_router.post("/", response_model=Optional[BuildingOut])
async def create(
    building_data: BuildingIn, db_session: AsyncSession = Depends(get_session)
):
    return await BuildingService(db_session).create(building_data)


@building_router.get("/", response_model=Optional[list[BuildingOut]])
async def get_all(
    name: Optional[str] = None,
    faculty_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = BuildingFilter(name=name, faculty_id=faculty_id)
    return await BuildingService(db_session).get_all(filters)


@building_router.get("/{building_id}", response_model=Optional[BuildingOut])
async def get_by_id(building_id: int, db_session: AsyncSession = Depends(get_session)):
    return await BuildingService(db_session).get_by_id(building_id)


@building_router.put("/{building_id}", response_model=Optional[BuildingOut])
async def update(
    building_id: int,
    building_data: BuildingIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await BuildingService(db_session).update(building_id, building_data)


@building_router.delete("/{building_id}", response_model=str)
async def delete(building_id: int, db_session: AsyncSession = Depends(get_session)):
    return await BuildingService(db_session).delete(building_id)


@building_router.get("/count/entities", response_model=Optional[int])
async def count(
    name: Optional[str] = None,
    faculty_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = BuildingFilter(name=name, faculty_id=faculty_id)
    return await BuildingService(db_session).count(filters)
