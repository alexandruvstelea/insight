from ...database.models.session import Session
from ...database.models.weeks import Week
from .schemas import SessionOut, SessionOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select, and_, or_
from datetime import datetime
from ..weeks.utils import get_week_from_timestamp


def session_to_out(session: Session) -> SessionOut:
    from ..rooms.utils import room_to_minimal
    from ..subjects.utils import subject_to_minimal

    return SessionOut(
        id=session.id,
        type=session.type,
        semester=session.semester,
        week_type=session.week_type,
        start=session.start,
        end=session.end,
        day=session.day,
        room=room_to_minimal(session.room),
        subject=subject_to_minimal(session.subject),
    )


def session_to_minimal(session: Session) -> SessionOutMinimal:
    return SessionOutMinimal(
        id=session.id,
        type=session.type,
        semester=session.semester,
        week_type=session.week_type,
        start=session.start,
        end=session.end,
        day=session.day,
    )


async def id_to_session(db_session: AsyncSession, session_id: int) -> Session:
    session = await db_session.get(Session, session_id)
    if session:
        return session
    raise HTTPException(status_code=404, detail=f"No session with id={session_id}.")


async def ids_to_sessions(
    db_session: AsyncSession, session_ids: List[int]
) -> List[Session]:
    result = await db_session.execute(
        select(Session).where(Session.id.in_(session_ids))
    )
    sessions = result.scalars().all()
    if len(sessions) != len(session_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more sessions not found for IDs {session_ids}",
        )
    return list(sessions)


async def is_session_overlap(
    db_session: AsyncSession, new_session: Session, current_session_id: int = -1
) -> bool:
    query = select(Session).where(
        and_(
            Session.id != current_session_id,
            Session.room_id == new_session.room_id,
            Session.day == new_session.day,
            Session.week_type == new_session.week_type,
            Session.semester == new_session.semester,
            or_(
                and_(
                    Session.start <= new_session.start, Session.end > new_session.start
                ),
                and_(Session.start < new_session.end, Session.end >= new_session.end),
                and_(
                    Session.start >= new_session.start, Session.end <= new_session.end
                ),
            ),
        )
    )
    result = await db_session.execute(query)
    existing_sessions = result.scalars().all()
    return len(existing_sessions) > 0


async def get_session_from_timestamp(
    db_session: AsyncSession, timestamp: datetime, room_id: int
) -> Session:
    week: Week = await get_week_from_timestamp(db_session, timestamp)
    result = await db_session.execute(
        select(Session).where(
            Session.semester == week.semester,
            Session.day == timestamp.weekday(),
            Session.start <= timestamp.time(),
            Session.end >= timestamp.time(),
            Session.room_id == room_id,
            or_(Session.week_type == 0, Session.week_type == week.id % 2),
        )
    )
    current_session = result.scalars().first()
    if current_session:
        return current_session
    raise HTTPException(
        status_code=404,
        detail=f"Could not find current session for timestamp {timestamp} and room_id {room_id}.",
    )
