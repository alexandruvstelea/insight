from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.session import Session
from .schemas import SessionOut, SessionIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import session_to_out, is_session_overlap
from ..rooms.utils import id_to_room
from ..subjects.utils import id_to_subject, get_subject_semester
import logging

logger = logging.getLogger(__name__)


class SessionOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sessions(self, faculty_id: int) -> List[SessionOut]:
        try:
            if faculty_id:
                logger.info(
                    f"Retrieving all sessions from database with faculty ID {faculty_id}."
                )
                query = (
                    select(Session)
                    .options(joinedload(Session.room), joinedload(Session.subject))
                    .where(Session.faculty_id == faculty_id)
                )
            else:
                logger.info("Retrieving all sessions from database.")
                query = select(Session).options(
                    joinedload(Session.room), joinedload(Session.subject)
                )
            result = await self.session.execute(query)
            sessions = result.scalars().unique().all()
            if sessions:
                logger.info("Succesfully retrieved all sessions from database.")
                return [
                    session_to_out(session)
                    for session in sorted(list(sessions), key=lambda x: x.start)
                ]
            logger.error("No sessions found.")
            raise HTTPException(status_code=404, detail="No sessions found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving sessions:\n{e}"
            )
            raise e

    async def get_session_by_id(self, id: int) -> SessionOut:
        session = await self.session.get(Session, id)
        try:
            logger.info(f"Retrieving session with ID {id} from database.")
            if session:
                logger.info(
                    f"Succesfully retrieved session with ID {id} from database."
                )
                return session_to_out(session)
            logger.error(f"No session with ID {id} found in database.")
            raise HTTPException(status_code=404, detail=f"No session with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving session with ID {id}:\n{e}"
            )
            raise e

    async def add_session(self, session_data: SessionIn) -> SessionOut:
        try:
            logger.info(f"Adding to database session {session_data}.")
            new_session = Session(
                type=session_data.type,
                semester=await get_subject_semester(
                    self.session, session_data.subject_id
                ),
                week_type=session_data.week_type,
                start=session_data.start,
                end=session_data.end,
                day=session_data.day,
                room_id=session_data.room_id,
                subject_id=session_data.subject_id,
            )
            new_session.room = await id_to_room(self.session, session_data.room_id)
            new_session.subject = await id_to_subject(
                self.session, session_data.subject_id
            )
            new_session.subject = await id_to_subject(
                self.session, session_data.subject_id
            )
            if session_data.faculty_id in new_session.subject.faculties_ids:
                new_session.faculty_id = session_data.faculty_id
            else:
                logger.error(
                    f"The given faculty ID {session_data.faculty_id} is not in the list of the session' subject faculties_ids."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"The given faculty ID {session_data.faculty_id} is not in the list of the session' subject faculties_ids.",
                )
            if await is_session_overlap(self.session, new_session):
                logger.error("The new session interval overlaps with an existing one.")
                raise HTTPException(
                    status_code=409,
                    detail="The new session interval overlaps with an existing one.",
                )
            self.session.add(new_session)
            await self.session.commit()
            await self.session.refresh(new_session)
            logger.info("Succesfully added new session to database.")
            return session_to_out(new_session)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding session to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding session to databse:\n{e}"
            )
            raise e

    async def update_session(self, id: int, new_session_data: SessionIn) -> SessionOut:
        try:
            logger.info(
                f"Updating session with ID {id} with new data: {new_session_data}."
            )
            session = await self.session.get(Session, id)
            if session:
                session.type = new_session_data.type
                session.semester = await get_subject_semester(
                    self.session, new_session_data.subject_id
                )
                session.week_type = new_session_data.week_type
                session.start = new_session_data.start
                session.end = new_session_data.end
                session.day = new_session_data.day
                session.room_id = new_session_data.room_id
                session.subject_id = new_session_data.subject_id
                session.room = await id_to_room(self.session, new_session_data.room_id)
                session.subject = await id_to_subject(
                    self.session, new_session_data.subject_id
                )
            if new_session_data.faculty_id in session.subject.faculties_ids:
                session.faculty_id = new_session_data.faculty_id
                if await is_session_overlap(self.session, session, id):
                    logger.error(
                        "The new session interval overlaps with an existing one."
                    )
                    raise HTTPException(
                        status_code=409,
                        detail="The new session interval overlaps with an existing one.",
                    )
                await self.session.commit()
                logger.info(f"Succesfully updated session with ID {id}.")
                return session_to_out(session)
            logger.error(f"No session with ID {id}")
            raise HTTPException(status_code=404, detail=f"No session with ID {id}.")
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while updating session with ID {id}:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating session with ID {id}:\n{e}"
            )
            raise e

    async def delete_session(self, id: int):
        try:
            logger.info(f"Deleting session with ID {id}.")
            session = await self.session.get(Session, id)
            if session:
                await self.session.delete(session)
                await self.session.commit()
                logger.info(f"Succesfully deleted session with ID {id}.")
                return JSONResponse(f"Session with ID={id} deleted.")
            logger.error(f"No session with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No session with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting session with ID {id}:\n{e}"
            )
            raise e
