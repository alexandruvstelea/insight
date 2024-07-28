from ...database.main import get_session
from fastapi import APIRouter, Depends, Header, Request
from .schemas import FacultyIn, FacultyOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import FacultyOperations
from http import HTTPStatus
from ...limiter import limiter
from typing import List
import logging

logger = logging.getLogger(__name__)
faculties_router = APIRouter(prefix="/api/faculties")


@faculties_router.get("/", response_model=List[FacultyOut], status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_faculties(
    request: Request,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[FacultyOut]:
    logger.info(f"Received GET request on endpoint /api/faculties from IP {client_ip}.")
    faculties = await FacultyOperations(session).get_faculties()
    return faculties


@faculties_router.get("/{id}", response_model=FacultyOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_faculty_by_id(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_session),
    client_ip: str = Header(None, alias="X-Real-IP"),
) -> FacultyOut:
    logger.info(
        f"Received GET request on endpoint /api/faculties/id from IP {client_ip}."
    )
    faculty = await FacultyOperations(session).get_faculty_by_id(id)
    return faculty


@faculties_router.post("/", response_model=FacultyOut, status_code=HTTPStatus.CREATED)
@limiter.limit("50/minute")
async def add_faculty(
    request: Request,
    faculty_data: FacultyIn,
    session: AsyncSession = Depends(get_session),
    client_ip: str = Header(None, alias="X-Real-IP"),
) -> FacultyOut:
    logger.info(
        f"Received POST request on endpoint /api/faculties from IP {client_ip}."
    )
    response = await FacultyOperations(session).add_faculty(faculty_data)
    return response


@faculties_router.put("/{id}", response_model=FacultyOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def update_faculty(
    request: Request,
    id: int,
    new_faculty_data: FacultyIn,
    session: AsyncSession = Depends(get_session),
    client_ip: str = Header(None, alias="X-Real-IP"),
) -> FacultyOut:
    logger.info(
        f"Received PUT request on endpoint /api/faculties/id from IP {client_ip}."
    )
    response = await FacultyOperations(session).update_faculty(id, new_faculty_data)
    return response


@faculties_router.delete("/{id}", status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def delete_faculty(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_session),
    client_ip: str = Header(None, alias="X-Real-IP"),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/faculties/id from IP {client_ip}."
    )
    response = await FacultyOperations(session).delete_faculty(id)
    return response
