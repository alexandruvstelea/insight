from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import SubjectIn, SubjectOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import SubjectOperations
from http import HTTPStatus
from typing import List

subjects_router = APIRouter(prefix="/api/subjects")


@subjects_router.get("/", response_model=List[SubjectOut], status_code=HTTPStatus.OK)
async def get_subjects(
    session: AsyncSession = Depends(get_session),
) -> List[SubjectOut]:
    response = await SubjectOperations(session).get_subjects()
    return response


@subjects_router.get("/{id}", response_model=SubjectOut, status_code=HTTPStatus.OK)
async def get_subject_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> SubjectOut:
    response = await SubjectOperations(session).get_subject_by_id(id)
    return response


@subjects_router.post("/", response_model=SubjectOut, status_code=HTTPStatus.CREATED)
async def add_subject(
    subject_data: SubjectIn, session: AsyncSession = Depends(get_session)
) -> SubjectOut:
    response = await SubjectOperations(session).add_subject(subject_data)
    return response


@subjects_router.put("/{id}", response_model=SubjectOut, status_code=HTTPStatus.OK)
async def update_subject(
    id: int, new_subject_data: SubjectIn, session: AsyncSession = Depends(get_session)
) -> SubjectOut:
    response = await SubjectOperations(session).update_subject(id, new_subject_data)
    return response


@subjects_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_subject(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await SubjectOperations(session).delete_subject(id)
    return response
