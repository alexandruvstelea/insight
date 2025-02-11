from app.repositories.interfaces.i_week_repository import IWeekRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from app.models.week import Week
from app.schemas.week import WeekFilter
from typing import Optional
from app.core.logging import logger


class WeekRepository(IWeekRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, week: Week) -> Optional[Week]:
        new_week = Week(start=week.start, end=week.end, semester=week.semester)

        self.session.add(new_week)
        await self.session.commit()
        await self.session.refresh(new_week)

        return new_week

    async def get_all(self, filters: Optional[WeekFilter]) -> Optional[list[Week]]:
        conditions = []

        if filters.start:
            conditions.append(Week.start >= filters.start)
        if filters.end:
            conditions.append(Week.end <= filters.end)
        if filters.semester:
            conditions.append(Week.semester == filters.semester)

        query = select(Week)
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        weeks = result.scalars().all()

        return weeks if weeks else None

    async def get_by_id(self, id: int) -> Optional[Week]:
        week = await self.session.get(Week, id)
        return week if week else None

    async def update(self, id: int, new_week: Week) -> Optional[Week]:
        week = await self.session.get(Week, id)

        if not week:
            return None

        week.start = new_week.start
        week.end = new_week.end
        week.semester = new_week.semester

        await self.session.commit()

        return week

    async def delete(self, id: int) -> bool:
        week = await self.session.get(Week, id)

        if not week:
            return False

        await self.session.delete(week)
        await self.session.commit()

        return True
