from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import ProgrammeIn, ProgrammeOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ProgrammeOperations
from http import HTTPStatus
from typing import List
import logging

logger = logging.getLogger(__name__)
programmes_router = APIRouter(prefix="/api/programmes")


@programmes_router.get(
    "/", response_model=List[ProgrammeOut], status_code=HTTPStatus.OK
)
async def get_programmes(
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[ProgrammeOut]:
    logger.info(
        f"Received GET request on endpoint /api/programmes from IP {client_ip}."
    )
    response = await ProgrammeOperations(session).get_programmes(faculty_id)
    return response


@programmes_router.get("/{id}", response_model=ProgrammeOut, status_code=HTTPStatus.OK)
async def get_programme_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProgrammeOut:
    logger.info(
        f"Received GET request on endpoint /api/programmes/id from IP {client_ip}."
    )
    response = await ProgrammeOperations(session).get_programme_by_id(id)
    return response


@programmes_router.post(
    "/", response_model=ProgrammeOut, status_code=HTTPStatus.CREATED
)
async def add_programme(
    programme_data: ProgrammeIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProgrammeOut:
    logger.info(
        f"Received POST request on endpoint /api/programmes from IP {client_ip}."
    )
    response = await ProgrammeOperations(session).add_programme(programme_data)
    return response


@programmes_router.put("/{id}", response_model=ProgrammeOut, status_code=HTTPStatus.OK)
async def update_programme(
    id: int,
    new_programme_data: ProgrammeIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProgrammeOut:
    logger.info(
        f"Received PUT request on endpoint /api/programmes/id from IP {client_ip}."
    )
    response = await ProgrammeOperations(session).update_programme(
        id, new_programme_data
    )
    return response


@programmes_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_programme(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/programmes/id from IP {client_ip}."
    )
    response = await ProgrammeOperations(session).delete_programme(id)
    return response
