from ...database.main import get_session
from fastapi import APIRouter, Depends, Header, Request
from .schemas import ProfessorIn, ProfessorOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ProfessorOperations
from http import HTTPStatus
from ...limiter import limiter
from typing import List
import logging

logger = logging.getLogger(__name__)
professors_router = APIRouter(prefix="/api/professors")


@professors_router.get(
    "/", response_model=List[ProfessorOut], status_code=HTTPStatus.OK
)
@limiter.limit("50/minute")
async def get_professors(
    request: Request,
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[ProfessorOut]:
    logger.info(
        f"Received GET request on endpoint /api/professors from IP {client_ip}."
    )
    professors = await ProfessorOperations(session).get_professors(faculty_id)
    return professors


@professors_router.get("/{id}", response_model=ProfessorOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_professor_by_id(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received GET request on endpoint /api/professors/id from IP {client_ip}."
    )
    professor = await ProfessorOperations(session).get_professor_by_id(id)
    return professor


@professors_router.post(
    "/", response_model=ProfessorOut, status_code=HTTPStatus.CREATED
)
@limiter.limit("50/minute")
async def add_professor(
    request: Request,
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
@limiter.limit("50/minute")
async def update_professor(
    request: Request,
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
@limiter.limit("50/minute")
async def delete_professor(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/professors/id from IP {client_ip}."
    )
    response = await ProfessorOperations(session).delete_professor(id)
    return response
