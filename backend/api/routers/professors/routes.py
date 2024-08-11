from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import ProfessorIn, ProfessorOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ProfessorOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)
professors_router = APIRouter(prefix="/api/professors")


@professors_router.get(
    "/",
    response_model=List[ProfessorOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_professors(
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[ProfessorOut]:
    logger.info(
        f"Received GET request on endpoint /api/professors from IP {client_ip}."
    )
    professors = await ProfessorOperations(session).get_professors(faculty_id)
    return professors


@professors_router.get(
    "/{id}",
    response_model=ProfessorOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_professor_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received GET request on endpoint /api/professors/id from IP {client_ip}."
    )
    professor = await ProfessorOperations(session).get_professor_by_id(id)
    return professor


# @authorize(role=["admin"])
@professors_router.post(
    "/",
    response_model=ProfessorOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_professor(
    professor_data: ProfessorIn,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ProfessorOut:
    logger.info(
        f"Received POST request on endpoint /api/professors from IP {client_ip}."
    )
    response = await ProfessorOperations(session).add_professor(professor_data)
    return response


# @authorize(role=["admin"])
@professors_router.put(
    "/{id}",
    response_model=ProfessorOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def update_professor(
    id: int,
    new_professor_data: ProfessorIn,
    # current_user: dict = Depends(get_current_user),
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


# @authorize(role=["admin"])
@professors_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_professor(
    id: int,
    # current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/professors/id from IP {client_ip}."
    )
    response = await ProfessorOperations(session).delete_professor(id)
    return response
