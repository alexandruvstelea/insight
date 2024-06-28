from ...database.main import get_session
from fastapi import APIRouter, Depends
from .schemas import SessionIn, SessionOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import SessionOperations
from http import HTTPStatus
from typing import List

sessions_router = APIRouter(prefix="/api/sessions")


@sessions_router.get("/", response_model=List[SessionOut], status_code=HTTPStatus.OK)
async def get_sessions(
    faculty_id: int = None,
    session: AsyncSession = Depends(get_session),
) -> List[SessionOut]:
    response = await SessionOperations(session).get_sessions(faculty_id)
    return response


@sessions_router.get("/{id}", response_model=SessionOut, status_code=HTTPStatus.OK)
async def get_session_by_id(
    id: int, session: AsyncSession = Depends(get_session)
) -> SessionOut:
    response = await SessionOperations(session).get_session_by_id(id)
    return response


@sessions_router.post("/", response_model=SessionOut, status_code=HTTPStatus.CREATED)
async def add_session(
    session_data: SessionIn, session: AsyncSession = Depends(get_session)
) -> SessionOut:
    response = await SessionOperations(session).add_session(session_data)
    return response


@sessions_router.put("/{id}", response_model=SessionOut, status_code=HTTPStatus.OK)
async def update_session(
    id: int, new_session_data: SessionIn, session: AsyncSession = Depends(get_session)
) -> SessionOut:
    response = await SessionOperations(session).update_session(id, new_session_data)
    return response


@sessions_router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_session(id: int, session: AsyncSession = Depends(get_session)) -> str:
    response = await SessionOperations(session).delete_session(id)
    return response
