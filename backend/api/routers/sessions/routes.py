from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import SessionIn, SessionOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import SessionOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)
sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get(
    "/",
    response_model=List[SessionOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_sessions(
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    db_session: AsyncSession = Depends(get_session),
) -> List[SessionOut]:
    logger.info(f"Received GET request on endpoint /api/sessions from IP {client_ip}.")
    sessions = await SessionOperations(db_session).get_sessions(faculty_id)
    return sessions


@sessions_router.get(
    "/{id}",
    response_model=SessionOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_session_by_id(
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    db_session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(
        f"Received GET request on endpoint /api/sessions/id from IP {client_ip}."
    )
    session = await SessionOperations(db_session).get_session_by_id(id)
    return session


@authorize(role=["admin"])
@sessions_router.post(
    "/",
    response_model=SessionOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.CREATED,
)
async def add_session(
    session_data: SessionIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(f"Received POST request on endpoint /api/sessions from IP {client_ip}.")
    response = await SessionOperations(session).add_session(session_data)
    return response


@authorize(role=["admin"])
@sessions_router.put(
    "/{id}",
    response_model=SessionOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def update_session(
    id: int,
    new_session_data: SessionIn,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(
        f"Received PUT request on endpoint /api/sessions/id from IP {client_ip}."
    )
    response = await SessionOperations(session).update_session(id, new_session_data)
    return response


@authorize(role=["admin"])
@sessions_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_session(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/sessions/id from IP {client_ip}."
    )
    response = await SessionOperations(session).delete_session(id)
    return response
