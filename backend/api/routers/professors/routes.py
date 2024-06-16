from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import ProfessorIn, ProfessorOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ProfessorOperations
from http import HTTPStatus
from typing import List

professors_router = APIRouter(prefix="/api/professors")


@professors_router.get(
    "/", response_model=List[ProfessorOut], status_code=HTTPStatus.OK
)
async def get_professors(
    session: AsyncSession = Depends(get_session),
) -> List[ProfessorOut]:
    response = await ProfessorOperations(session).get_professors()
    return response


@professors_router.get("/{id}", response_model=ProfessorOut, status_code=HTTPStatus.OK)
async def get_professor_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> ProfessorOut:
    response = await ProfessorOperations(session).get_professor_by_id(id)
    return response


@professors_router.post(
    "/", response_model=ProfessorOut, status_code=HTTPStatus.CREATED
)
async def add_professor(
    professor_data: ProfessorIn, session: AsyncSession = Depends(get_session)
) -> ProfessorOut:
    response = await ProfessorOperations(session).add_professor(professor_data)
    return response


@professors_router.put("/{id}", response_model=ProfessorOut, status_code=HTTPStatus.OK)
async def update_professor(
    id: int,
    new_professor_data: ProfessorIn,
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    response = await ProfessorOperations(session).update_professor(
        id, new_professor_data
    )
    return response


@professors_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_professor(
    id: int, session: AsyncSession = Depends(get_session)
) -> str:
    response = await ProfessorOperations(session).delete_professor(id)
    return response
