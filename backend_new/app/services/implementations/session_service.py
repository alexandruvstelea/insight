from app.services.interfaces.i_session_service import ISessionService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import Session
from app.schemas.session import SessionIn, SessionOut
from app.repositories.implementations.session_repository import SessionRepository
from app.repositories.implementations.room_repository import RoomRepository
from app.repositories.implementations.subject_repository import SubjectRepository
from typing import Optional
from app.schemas.session import SessionFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class SessionService(ISessionService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, session_data: SessionIn) -> Optional[SessionOut]:
        try:
            new_session = Session(
                type=session_data.type,
                week_type=session_data.week_type,
                start=session_data.start,
                end=session_data.end,
                day=session_data.day,
                room_id=session_data.room_id,
                subject_id=session_data.subject_id,
                faculty_id=session_data.faculty_id,
            )

            if session_data.room_id:
                new_session.room = await RoomRepository(self.session).get_by_id(
                    session_data.room_id
                )

            if session_data.subject_id:
                new_session.subject = await SubjectRepository(self.session).get_by_id(
                    session_data.subject_id
                )
                new_session.semester = new_session.subject.semester

            if not SessionRepository(self.session).__is_session_overlap(new_session):
                response = await self.repository.create(new_session)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New session overlaps with an existing session.",
                )

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new session.",
                )

            return SessionOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new session.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new session.",
            )

    async def get_all(
        self, filters: Optional[SessionFilter]
    ) -> Optional[list[SessionOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found."
                )

            return [SessionOut.model_validate(session) for session in response]

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving sessions.",
            )

    async def get_by_id(self, id: int) -> Optional[SessionOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No session found for ID={id}."
                )

            return SessionOut.model_validate(response)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving session with ID={id}.",
            )

    async def update(self, id: int, session_data: SessionIn) -> Optional[SessionOut]:
        try:
            new_session = Session(
                type=session_data.type,
                week_type=session_data.week_type,
                start=session_data.start,
                end=session_data.end,
                day=session_data.day,
                room_id=session_data.room_id,
                subject_id=session_data.subject_id,
                faculty_id=session_data.faculty_id,
            )

            if session_data.room_id:
                new_session.room = await RoomRepository(self.session).get_by_id(
                    session_data.room_id
                )

            if session_data.subject_id:
                new_session.subject = await SubjectRepository(self.session).get_by_id(
                    session_data.subject_id
                )
                new_session.semester = new_session.subject.semester

            if not SessionRepository(self.session).__is_session_overlap(new_session):
                response = await self.repository.update(id, new_session)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New session overlaps with an existing session.",
                )

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while updating session.",
                )

            return SessionOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating session with ID={id}.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating session with ID={id}.{e}",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No session with ID={id} found.",
                )
            return JSONResponse(f"Session with ID {id} deleted.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting session with ID={id}.",
            )

    async def count(self, filters: Optional[SessionFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting sessions.",
            )
