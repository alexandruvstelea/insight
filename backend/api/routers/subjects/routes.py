from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import SubjectIn, SubjectOut
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter
from .operations import SubjectOperations
from http import HTTPStatus
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)
subjects_router = APIRouter(prefix="/api/subjects")


@subjects_router.get(
    "/",
    response_model=List[SubjectOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_subjects(
    faculty_id: int = None,
    professor_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[SubjectOut]:
    logger.info(f"Received GET request on endpoint /api/subjects from IP {client_ip}.")
    subjects = await SubjectOperations(session).get_subjects(faculty_id, professor_id)
    return subjects


@subjects_router.get(
    "/{id}",
    response_model=SubjectOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_subject_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(
        f"Received GET request on endpoint /api/subjects/id from IP {client_ip}."
    )
    subject = await SubjectOperations(session).get_subject_by_id(id)
    return subject


@authorize(role=["admin"])
@subjects_router.post(
    "/",
    response_model=SubjectOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_subject(
    subject_data: SubjectIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(f"Received POST request on endpoint /api/subjects from IP {client_ip}.")
    response = await SubjectOperations(session).add_subject(subject_data)
    return response


@authorize(role=["admin"])
@subjects_router.put(
    "/{id}",
    response_model=SubjectOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def update_subject(
    id: int,
    new_subject_data: SubjectIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SubjectOut:
    logger.info(
        f"Received PUT request on endpoint /api/subjects/id from IP {client_ip}."
    )
    response = await SubjectOperations(session).update_subject(id, new_subject_data)
    return response


@authorize(role=["admin"])
@subjects_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_subject(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/subjects/id from IP {client_ip}."
    )
    response = await SubjectOperations(session).delete_subject(id)
    return response
