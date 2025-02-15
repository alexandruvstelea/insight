from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.programme import ProgrammeIn, ProgrammeOut, ProgrammeFilter
from app.services.implementations.programme_service import ProgrammeService
from app.core.database import get_session
from typing import Optional, Literal
from app.core.logging import logger

programme_router = APIRouter(prefix="/programme", tags=["programme"])


@programme_router.post("/", response_model=Optional[ProgrammeOut])
async def create(
    programme_data: ProgrammeIn, db_session: AsyncSession = Depends(get_session)
):
    return await ProgrammeService(db_session).create(programme_data)


@programme_router.get("/", response_model=Optional[list[ProgrammeOut]])
async def get_all(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    type: Optional[Literal["bachelor", "master", "phd"]] = None,
    faculty_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ProgrammeFilter(
        name=name,
        abbreviation=abbreviation,
        type=type,
        faculty_id=faculty_id,
        subject_id=subject_id,
    )

    return await ProgrammeService(db_session).get_all(filters)


@programme_router.get("/{programme_id}", response_model=Optional[ProgrammeOut])
async def get_by_id(programme_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ProgrammeService(db_session).get_by_id(programme_id)


@programme_router.put("/{programme_id}", response_model=Optional[ProgrammeOut])
async def update(
    programme_id: int,
    programme_data: ProgrammeIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await ProgrammeService(db_session).update(programme_id, programme_data)


@programme_router.delete("/{programme_id}", response_model=str)
async def delete(programme_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ProgrammeService(db_session).delete(programme_id)


@programme_router.get("/count/entities", response_model=Optional[int])
async def count(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    type: Optional[Literal["bachelor", "master", "phd"]] = None,
    faculty_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ProgrammeFilter(
        name=name,
        abbreviation=abbreviation,
        type=type,
        faculty_id=faculty_id,
        subject_id=subject_id,
    )

    return await ProgrammeService(db_session).count(filters)
