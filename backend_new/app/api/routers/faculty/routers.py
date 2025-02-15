from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.faculty import FacultyIn, FacultyOut, FacultyFilter
from app.services.implementations.faculty_service import FacultyService
from app.core.database import get_session
from typing import Optional
from app.core.logging import logger

faculty_router = APIRouter(prefix="/faculty", tags=["faculty"])


@faculty_router.post("/", response_model=Optional[FacultyOut])
async def create(
    faculty_data: FacultyIn, db_session: AsyncSession = Depends(get_session)
):
    return await FacultyService(db_session).create(faculty_data)


@faculty_router.get("/", response_model=Optional[list[FacultyOut]])
async def get_all(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    building_id: Optional[int] = None,
    professor_id: Optional[int] = None,
    programme_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = FacultyFilter(
        name=name,
        abbreviation=abbreviation,
        building_id=building_id,
        professor_id=professor_id,
        programme_id=programme_id,
    )
    return await FacultyService(db_session).get_all(filters)


@faculty_router.get("/{faculty_id}", response_model=Optional[FacultyOut])
async def get_by_id(faculty_id: int, db_session: AsyncSession = Depends(get_session)):
    return await FacultyService(db_session).get_by_id(faculty_id)


@faculty_router.put("/{faculty_id}", response_model=Optional[FacultyOut])
async def update(
    faculty_id: int,
    faculty_data: FacultyIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await FacultyService(db_session).update(faculty_id, faculty_data)


@faculty_router.delete("/{faculty_id}", response_model=str)
async def delete(faculty_id: int, db_session: AsyncSession = Depends(get_session)):
    return await FacultyService(db_session).delete(faculty_id)


@faculty_router.get("/count/entities", response_model=Optional[int])
async def count(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    building_id: Optional[int] = None,
    professor_id: Optional[int] = None,
    programme_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = FacultyFilter(
        name=name,
        abbreviation=abbreviation,
        building_id=building_id,
        professor_id=professor_id,
        programme_id=programme_id,
    )
    return await FacultyService(db_session).count(filters)
