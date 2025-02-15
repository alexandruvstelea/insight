from app.repositories.interfaces.i_session_repository import ISessionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.models.session import Session
from app.schemas.session import SessionFilter
from typing import Optional
from app.core.logging import logger


class SessionRepository(ISessionRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, session: Session) -> Optional[Session]:
        try:
            self.session.add(session)
            await self.session.commit()
            await self.session.refresh(session)
            return session
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self, filters: Optional[SessionFilter]
    ) -> Optional[list[Session]]:
        try:
            query = select(Session).options(joinedload(Session.subject))

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            sessions = result.scalars().all()

            return sessions if sessions else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Session]:
        try:
            session = await self.session.get(Session, id)
            return session if session else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_session: Session) -> Optional[Session]:
        try:
            session = await self.session.get(Session, id)

            if not session:
                return None

            session.type = new_session.type
            session.semester = new_session.semester
            session.week_type = new_session.week_type
            session.start = new_session.start
            session.end = new_session.end
            session.day = new_session.day
            session.room_id = new_session.room_id
            session.room = new_session.room
            session.subject_id = new_session.subject_id
            session.subject = new_session.subject
            session.faculty_id = new_session.faculty_id

            await self.session.commit()

            return session
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            session = await self.session.get(Session, id)

            if not session:
                return False

            await self.session.delete(session)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[SessionFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Session)

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def _get_conditions(self, filters: SessionFilter) -> Optional[list]:
        conditions = []

        if filters.type:
            conditions.append(Session.type == filters.type)
        if filters.semester:
            conditions.append(Session.semester == filters.semester)
        if filters.type:
            conditions.append(Session.type == filters.type)
        if filters.week_type:
            conditions.append(Session.week_type == filters.week_type)
        if filters.start:
            conditions.append(Session.start >= filters.start)
        if filters.end:
            conditions.append(Session.end <= filters.end)
        if filters.day:
            conditions.append(Session.day == filters.day)

        return conditions if conditions else None
        # new_session = Session(
        #     type=session.type,
        #     semester=session.semester,
        #     week_type=session.week_type,
        #     start=session.start,
        #     end=session.end,
        #     day=session.day,
        #     room_id=session.room_id,
        #     room=session.room,
        #     subject_id=session.subject_id,
        #     subject=session.subject,
        #     faculty_id=session.faculty_id,
        # )
