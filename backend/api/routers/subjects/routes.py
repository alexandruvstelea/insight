from ...database.main import get_session
from fastapi import APIRouter, Depends, Header, Request
from .schemas import SubjectIn, SubjectOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import SubjectOperations
from http import HTTPStatus
from ...limiter import limiter
from typing import List
import logging

logger = logging.getLogger(__name__)
subjects_router = APIRouter(prefix="/api/subjects")


@subjects_router.get("/", response_model=List[SubjectOut], status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_subjects(
    request: Request,
    faculty_id: int = None,
    professor_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[SubjectOut]:
    logger.info(f"Received GET request on endpoint /api/subjects from IP {client_ip}.")
    subjects = await SubjectOperations(session).get_subjects(faculty_id, professor_id)
    return subjects


@subjects_router.get("/{id}", response_model=SubjectOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_subject_by_id(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(
        f"Received GET request on endpoint /api/subjects/id from IP {client_ip}."
    )
    subject = await SubjectOperations(session).get_subject_by_id(id)
    return subject


@subjects_router.post("/", response_model=SubjectOut, status_code=HTTPStatus.CREATED)
@limiter.limit("50/minute")
async def add_subject(
    request: Request,
    subject_data: SubjectIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(f"Received POST request on endpoint /api/subjects from IP {client_ip}.")
    response = await SubjectOperations(session).add_subject(subject_data)
    return response


@subjects_router.put("/{id}", response_model=SubjectOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def update_subject(
    request: Request,
    id: int,
    new_subject_data: SubjectIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(
        f"Received PUT request on endpoint /api/subjects/id from IP {client_ip}."
    )
    response = await SubjectOperations(session).update_subject(id, new_subject_data)
    return response


@subjects_router.delete("/{id}", status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def delete_subject(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/subjects/id from IP {client_ip}."
    )
    response = await SubjectOperations(session).delete_subject(id)
    return response
