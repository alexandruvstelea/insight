from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.session import SessionIn, SessionOut, SessionFilter
from app.services.implementations.session_service import SessionService
from app.core.database import get_session
from typing import Optional, Literal
from datetime import time
from app.core.logging import logger

session_router = APIRouter(prefix="/session", tags=["session"])


@session_router.post("/", response_model=Optional[SessionOut])
async def create(
    subject_data: SessionIn, db_session: AsyncSession = Depends(get_session)
):
    return await SessionService(db_session).create(subject_data)


@session_router.get("/", response_model=Optional[list[SessionOut]])
async def get_all(
    type: Optional[Literal["course", "laboratory", "project", "seminar"]] = None,
    semester: Optional[Literal[1, 2]] = None,
    week_type: Optional[Literal[0, 1, 2]] = None,
    start: Optional[time] = None,
    end: Optional[time] = None,
    day: Optional[Literal[0, 1, 2, 3, 4, 5, 6]] = None,
    room_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    faculty_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):

    filters = SessionFilter(
        type=type,
        semester=semester,
        week_type=week_type,
        start=start,
        end=end,
        day=day,
        room_id=room_id,
        subject_id=subject_id,
        faculty_id=faculty_id,
    )

    return await SessionService(db_session).get_all(filters)


@session_router.get("/{session_id}", response_model=Optional[SessionOut])
async def get_by_id(session_id: int, db_session: AsyncSession = Depends(get_session)):
    return await SessionService(db_session).get_by_id(session_id)


@session_router.put("/{session_id}", response_model=Optional[SessionOut])
async def update(
    session_id: int,
    subject_data: SessionIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await SessionService(db_session).update(session_id, subject_data)


@session_router.delete("/{session_id}", response_model=str)
async def delete(session_id: int, db_session: AsyncSession = Depends(get_session)):
    return await SessionService(db_session).delete(session_id)


@session_router.get("/count/entities", response_model=Optional[int])
async def count(
    type: Optional[Literal["course", "laboratory", "project", "seminar"]] = None,
    semester: Optional[Literal[1, 2]] = None,
    week_type: Optional[Literal[0, 1, 2]] = None,
    start: Optional[time] = None,
    end: Optional[time] = None,
    day: Optional[Literal[0, 1, 2, 3, 4, 5, 6]] = None,
    room_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    faculty_id: Optional[int] = None,
    db_session: AsyncSession = Depends(get_session),
):

    filters = SessionFilter(
        type=type,
        semester=semester,
        week_type=week_type,
        start=start,
        end=end,
        day=day,
        room_id=room_id,
        subject_id=subject_id,
        faculty_id=faculty_id,
    )

    return await SessionService(db_session).count(filters)
