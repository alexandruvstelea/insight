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


class SessionOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sessions(self) -> List[SessionOut]:
        try:
            query = select(Session).options(
                joinedload(Session.room), joinedload(Session.subject)
            )
            result = await self.session.execute(query)
            sessions = result.scalars().unique().all()
            if sessions:
                return [
                    session_to_out(session)
                    for session in sorted(list(sessions), key=lambda x: x.start)
                ]
            raise HTTPException(status_code=404, detail="No sessions found.")
        except Exception as e:
            raise e

    async def get_session_by_id(self, id: int) -> SessionOut:
        session = await self.session.get(Session, id)
        try:
            if session:
                return session_to_out(session)
            raise HTTPException(status_code=404, detail=f"No session with id={id}.")
        except Exception as e:
            raise e

    async def add_session(self, session_data: SessionIn) -> SessionOut:
        try:
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
            new_session.faculties_ids = new_session.subject.faculties_ids
            if is_session_overlap(self.session, new_session):
                raise HTTPException(
                    status_code=409,
                    detail="The new session interval overlaps with an existing one.",
                )
            self.session.add(new_session)
            await self.session.commit()
            await self.session.refresh(new_session)
            return session_to_out(new_session)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_session(self, id: int, new_session_data: SessionIn) -> SessionOut:
        try:
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
                session.faculties_ids = session.subject.faculties_ids
                if is_session_overlap(self.session, session):
                    raise HTTPException(
                        status_code=409,
                        detail="The new session interval overlaps with an existing one.",
                    )
                await self.session.commit()
                return session_to_out(session)
            raise HTTPException(status_code=404, detail=f"No session with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_session(self, id: int):
        try:
            session = await self.session.get(Session, id)
            if session:
                await self.session.delete(session)
                await self.session.commit()
                return JSONResponse(f"Session with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No session with id={id}.")
        except Exception as e:
            raise e
