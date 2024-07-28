from ...database.main import get_session
from fastapi import APIRouter, Depends, Header, Request
from .schemas import SessionIn, SessionOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import SessionOperations
from http import HTTPStatus
from ...limiter import limiter
from typing import List
import logging

logger = logging.getLogger(__name__)
sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get("/", response_model=List[SessionOut], status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_sessions(
    request: Request,
    faculty_id: int = None,
    client_ip: str = Header(None, alias="X-Real-IP"),
    db_session: AsyncSession = Depends(get_session),
) -> List[SessionOut]:
    logger.info(f"Received GET request on endpoint /api/sessions from IP {client_ip}.")
    sessions = await SessionOperations(db_session).get_sessions(faculty_id)
    return sessions


@sessions_router.get("/{id}", response_model=SessionOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def get_session_by_id(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    db_session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(
        f"Received GET request on endpoint /api/sessions/id from IP {client_ip}."
    )
    session = await SessionOperations(db_session).get_session_by_id(id)
    return session


@sessions_router.post("/", response_model=SessionOut, status_code=HTTPStatus.CREATED)
@limiter.limit("50/minute")
async def add_session(
    request: Request,
    session_data: SessionIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(f"Received POST request on endpoint /api/sessions from IP {client_ip}.")
    response = await SessionOperations(session).add_session(session_data)
    return response


@sessions_router.put("/{id}", response_model=SessionOut, status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def update_session(
    request: Request,
    id: int,
    new_session_data: SessionIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> SessionOut:
    logger.info(
        f"Received PUT request on endpoint /api/sessions/id from IP {client_ip}."
    )
    response = await SessionOperations(session).update_session(id, new_session_data)
    return response


@sessions_router.delete("/{id}", status_code=HTTPStatus.OK)
@limiter.limit("50/minute")
async def delete_session(
    request: Request,
    id: int,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/sessions/id from IP {client_ip}."
    )
    response = await SessionOperations(session).delete_session(id)
    return response
