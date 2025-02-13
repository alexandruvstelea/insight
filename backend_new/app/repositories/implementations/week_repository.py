from app.repositories.interfaces.i_week_repository import IWeekRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from app.models.week import Week
from app.schemas.week import WeekFilter
from typing import Optional
from app.core.logging import logger


class WeekRepository(IWeekRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, week: Week) -> Optional[Week]:
        try:
            self.session.add(week)
            await self.session.commit()
            await self.session.refresh(week)
            return week
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(self, filters: Optional[WeekFilter]) -> Optional[list[Week]]:
        try:
            query = select(Week)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            weeks = result.scalars().all()

            return weeks if weeks else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Week]:
        try:
            week = await self.session.get(Week, id)
            return week if week else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_week: Week) -> Optional[Week]:
        try:
            week = await self.session.get(Week, id)

            if not week:
                return None

            week.start = new_week.start
            week.end = new_week.end
            week.semester = new_week.semester

            await self.session.commit()

            return week
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            week = await self.session.get(Week, id)

            if not week:
                return False

            await self.session.delete(week)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[WeekFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Week)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def __get_conditions(filters: WeekFilter) -> Optional[list]:
        conditions = []

        if filters.start:
            conditions.append(Week.start >= filters.start)
        if filters.end:
            conditions.append(Week.end <= filters.end)
        if filters.semester:
            conditions.append(Week.semester == filters.semester)

        return conditions if conditions else None
        # new_week = Week(start=week.start, end=week.end, semester=week.semester)
