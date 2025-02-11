from ...database.models.session import Session
from ...database.models.weeks import Week
from .schemas import SessionOut, SessionOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException
from sqlalchemy import select, and_, or_
from datetime import datetime
from ..weeks.utils import get_week_from_timestamp
import logging
import pytz

logger = logging.getLogger(__name__)


def session_to_out(session: Session) -> SessionOut:
    from ..rooms.utils import room_to_minimal
    from ..subjects.utils import subject_to_minimal

    if session:
        logger.info(f"Converting session with ID {session.id} to SessionOut format.")

        faculty_ids = []
        if session.subject:
            for programme in session.subject.programmes:
                if (
                    programme.faculty_id not in faculty_ids
                    and programme.faculty_id != None
                ):
                    faculty_ids.append(programme.faculty_id)

        return SessionOut(
            id=session.id,
            type=session.type,
            semester=session.semester,
            week_type=session.week_type,
            start=session.start,
            end=session.end,
            day=session.day,
            room=room_to_minimal(session.room),
            subject=subject_to_minimal(session.subject) if session.subject else None,
            faculty_ids=faculty_ids,
        )
    return None


def session_to_minimal(session: Session) -> SessionOutMinimal:
    if session:
        logger.info(
            f"Converting session with ID {session.id} to SessionOutMinimal format."
        )
        return SessionOutMinimal(
            id=session.id,
            type=session.type,
            semester=session.semester,
            week_type=session.week_type,
            start=session.start,
            end=session.end,
            day=session.day,
        )
    return None


async def id_to_session(db_session: AsyncSession, session_id: int) -> Session:
    try:
        if session_id:
            logger.info(f"Retrieving session for ID {session_id}.")
            session = await db_session.get(Session, session_id)
            if session:
                logger.info(f"Retrieved session with ID {session_id}.")
                return session
            logger.error(f"No session with ID {session_id}.")
            raise HTTPException(
                status_code=404, detail=f"No session with ID {session_id}."
            )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving session with ID {session_id}:\n{e}"
        )
        raise e


async def ids_to_sessions(
    db_session: AsyncSession, session_ids: List[int]
) -> List[Session]:
    try:
        if session_ids:
            logger.info(f"Retrieving sessions with IDs {session_ids}.")
            result = await db_session.execute(
                select(Session).where(Session.id.in_(session_ids))
            )
            sessions = result.scalars().all()
            if len(sessions) != len(session_ids):
                logger.error(f"One or more sessions not found for IDs {session_ids}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"One or more sessions not found for IDs {session_ids}",
                )
            logger.info(f"Retrieved sessions with IDs {session_ids}.")
            return list(sessions)
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving sessions with IDs {session_ids}:\n{e}"
        )
        raise e


async def is_session_overlap(
    db_session: AsyncSession, new_session: Session, current_session_id: int = -1
) -> bool:
    try:
        logger.info("Checking for session overlap.")
        query = select(Session).where(
            and_(
                Session.id != current_session_id,
                Session.room_id == new_session.room_id,
                Session.day == new_session.day,
                Session.week_type == new_session.week_type,
                Session.semester == new_session.semester,
                or_(
                    and_(
                        Session.start <= new_session.start,
                        Session.end > new_session.start,
                    ),
                    and_(
                        Session.start < new_session.end, Session.end >= new_session.end
                    ),
                    and_(
                        Session.start >= new_session.start,
                        Session.end <= new_session.end,
                    ),
                ),
            )
        )
        result = await db_session.execute(query)
        existing_sessions = result.scalars().all()
        return len(existing_sessions) > 0
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while checking for session overlap:\n{e}"
        )
        raise e


async def get_session_from_timestamp(
    db_session: AsyncSession, timestamp: datetime, room_id: int
) -> Session:
    try:

        ro_timezone = pytz.timezone("Europe/Bucharest")
        timestamp_ro = timestamp.astimezone(ro_timezone)

        logger.info(
            f"Retrieving session from timestamp {timestamp_ro} and room_id {room_id}."
        )

        week: Week = await get_week_from_timestamp(db_session, timestamp_ro)
        result = await db_session.execute(
            select(Session).where(
                Session.semester == week.semester,
                Session.day == timestamp_ro.weekday(),
                Session.start <= timestamp_ro.time(),
                Session.end >= timestamp_ro.time(),
                Session.room_id == room_id,
                or_(Session.week_type == 0, Session.week_type == week.id % 2),
            )
        )
        current_session = result.scalars().first()
        if current_session:
            return current_session
        logger.error(
            f"Could not find current session for timestamp {timestamp_ro} and room_id {room_id}."
        )
        raise HTTPException(
            status_code=404,
            detail=f"Could not find current session for timestamp {timestamp_ro}.",
        )
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving session from timestamp {timestamp_ro} and room_id {room_id}:\n{e}"
        )
        raise e


async def update_session_semester(
    db_session: AsyncSession, session_ids: List[int], new_semester: int
):
    if session_ids:
        try:
            for id in session_ids:
                session = await db_session.get(Session, id)
                if session.semester != new_semester:
                    logger.info(f"Updating semester of session with ID {id}.")
                    session.semester = new_semester
                    await db_session.commit()
                    logger.info(
                        f"Succesfully updated semester of session with ID {id} to SEMESTER {new_semester}."
                    )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating semester of session with ID {id}:\n{e}"
            )
            raise e
