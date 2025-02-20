from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.subject import SubjectIn, SubjectOut, SubjectFilter
from app.services.implementations.subject_service import SubjectService
from app.core.database import get_session
from typing import Optional, Literal
from app.core.logging import logger

subject_router = APIRouter(prefix="/subject", tags=["subject"])


@subject_router.post("/", response_model=Optional[SubjectOut])
async def create(
    subject_data: SubjectIn, db_session: AsyncSession = Depends(get_session)
):
    return await SubjectService(db_session).create(subject_data)


@subject_router.get("/", response_model=Optional[list[SubjectOut]])
async def get_all(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    semester: Optional[int] = Query(
        None, ge=1, le=2, description="Must be either 1 or 2"
    ),
    course_professor_id: Optional[int] = None,
    laboratory_professor_id: Optional[int] = None,
    seminar_professor_id: Optional[int] = None,
    project_professor_id: Optional[int] = None,
    programme_id: Optional[int] = None,
    session_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):

    filters = SubjectFilter(
        name=name,
        abbreviation=abbreviation,
        semester=semester,
        course_professor_id=course_professor_id,
        laboratory_professor_id=laboratory_professor_id,
        seminar_professor_id=seminar_professor_id,
        project_professor_id=project_professor_id,
        programme_id=programme_id,
        session_id=session_id,
    )

    return await SubjectService(db_session).get_all(filters)


@subject_router.get("/{subject_id}", response_model=Optional[SubjectOut])
async def get_by_id(subject_id: int, db_session: AsyncSession = Depends(get_session)):
    return await SubjectService(db_session).get_by_id(subject_id)


@subject_router.put("/{subject_id}", response_model=Optional[SubjectOut])
async def update(
    subject_id: int,
    subject_data: SubjectIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await SubjectService(db_session).update(subject_id, subject_data)


@subject_router.delete("/{subject_id}", response_model=str)
async def delete(subject_id: int, db_session: AsyncSession = Depends(get_session)):
    return await SubjectService(db_session).delete(subject_id)


@subject_router.get("/count/entities", response_model=Optional[int])
async def count(
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    semester: Optional[int] = Query(
        None, ge=1, le=2, description="Must be either 1 or 2"
    ),
    course_professor_id: Optional[int] = None,
    laboratory_professor_id: Optional[int] = None,
    seminar_professor_id: Optional[int] = None,
    project_professor_id: Optional[int] = None,
    programme_id: Optional[int] = None,
    session_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):

    filters = SubjectFilter(
        name=name,
        abbreviation=abbreviation,
        semester=semester,
        course_professor_id=course_professor_id,
        laboratory_professor_id=laboratory_professor_id,
        seminar_professor_id=seminar_professor_id,
        project_professor_id=project_professor_id,
        programme_id=programme_id,
        session_id=session_id,
    )

    return await SubjectService(db_session).count(filters)
