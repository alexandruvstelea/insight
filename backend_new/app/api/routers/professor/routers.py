from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.professor import ProfessorIn, ProfessorOut, ProfessorFilter
from app.services.implementations.professor_service import ProfessorService
from app.core.database import get_session
from typing import Optional, Literal
from app.core.logging import logger

professor_router = APIRouter(prefix="/professor", tags=["professor"])


@professor_router.post("/", response_model=Optional[ProfessorOut])
async def create(
    professor_data: ProfessorIn, db_session: AsyncSession = Depends(get_session)
):
    return await ProfessorService(db_session).create(professor_data)


@professor_router.get("/", response_model=Optional[list[ProfessorOut]])
async def get_all(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[Literal["male", "female"]] = None,
    professor_id: Optional[int] = None,
    course_id: Optional[int] = None,
    laboratory_id: Optional[int] = None,
    seminar_id: Optional[int] = None,
    project_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ProfessorFilter(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        professor_id=professor_id,
        course_id=course_id,
        laboratory_id=laboratory_id,
        seminar_id=seminar_id,
        project_id=project_id,
    )

    return await ProfessorService(db_session).get_all(filters)


@professor_router.get("/{professor_id}", response_model=Optional[ProfessorOut])
async def get_by_id(professor_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ProfessorService(db_session).get_by_id(professor_id)


@professor_router.put("/{professor_id}", response_model=Optional[ProfessorOut])
async def update(
    professor_id: int,
    professor_data: ProfessorIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await ProfessorService(db_session).update(professor_id, professor_data)


@professor_router.delete("/{professor_id}", response_model=str)
async def delete(professor_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ProfessorService(db_session).delete(professor_id)


@professor_router.get("/count/entities", response_model=Optional[int])
async def count(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[Literal["male", "female"]] = None,
    professor_id: Optional[int] = None,
    course_id: Optional[int] = None,
    laboratory_id: Optional[int] = None,
    seminar_id: Optional[int] = None,
    project_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ProfessorFilter(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        professor_id=professor_id,
        course_id=course_id,
        laboratory_id=laboratory_id,
        seminar_id=seminar_id,
        project_id=project_id,
    )

    return await ProfessorService(db_session).count(filters)
