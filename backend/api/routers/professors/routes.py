from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import ProfessorIn, ProfessorOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ProfessorOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
professors_router = APIRouter(prefix="/api/professors")


@professors_router.get(
    "/", response_model=List[ProfessorOut], status_code=HTTPStatus.OK
)
async def get_professors(
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[ProfessorOut]:
    logger.info(
        f"Received GET request on endpoint /api/professors from IP {client_ip}."
    )
    response = await ProfessorOperations(session).get_professors(faculty_id)
    return response


@professors_router.get("/{id}", response_model=ProfessorOut, status_code=HTTPStatus.OK)
async def get_professor_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received GET request on endpoint /api/professors/id from IP {client_ip}."
    )
    response = await ProfessorOperations(session).get_professor_by_id(id)
    return response


@professors_router.post(
    "/", response_model=ProfessorOut, status_code=HTTPStatus.CREATED
)
async def add_professor(
    professor_data: ProfessorIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received POST request on endpoint /api/professors from IP {client_ip}."
    )
    response = await ProfessorOperations(session).add_professor(professor_data)
    return response


@professors_router.put("/{id}", response_model=ProfessorOut, status_code=HTTPStatus.OK)
async def update_professor(
    id: int,
    new_professor_data: ProfessorIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received PUT request on endpoint /api/professors/id from IP {client_ip}."
    )
    response = await ProfessorOperations(session).update_professor(
        id, new_professor_data
    )
    return response


@professors_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_professor(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/professors/id from IP {client_ip}."
    )
    response = await ProfessorOperations(session).delete_professor(id)
    return response
