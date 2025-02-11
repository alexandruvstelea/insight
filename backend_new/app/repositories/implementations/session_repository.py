from app.repositories.interfaces.i_session_repository import ISessionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
from app.models.session import Session
from app.schemas.session import SessionFilter
from typing import Optional
from app.core.logging import logger


class SessionRepository(ISessionRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, session: Session) -> Optional[Session]:
        new_session = Session(
            type=session.type,
            semester=session.semester,
            week_type=session.week_type,
            start=session.start,
            end=session.end,
            day=session.day,
            room_id=session.room_id,
            room=session.room,
            subject_id=session.subject_id,
            subject=session.subject,
            faculty_id=session.faculty_id,
        )

        self.session.add(new_session)
        await self.session.commit()
        await self.session.refresh(new_session)

        return new_session

    async def get_all(
        self, filters: Optional[SessionFilter]
    ) -> Optional[list[Session]]:
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

        query = select(Session).options(joinedload(Session.subject))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        sessions = result.scalars().all()

        return sessions if sessions else None

    async def get_by_id(self, id: int) -> Optional[Session]:
        session = await self.session.get(Session, id)
        return session if session else None

    async def update(self, id: int, new_session: Session) -> Optional[Session]:
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

    async def delete(self, id: int) -> bool:
        session = await self.session.get(Session, id)

        if not session:
            return False

        await self.session.delete(session)
        await self.session.commit()

        return True
