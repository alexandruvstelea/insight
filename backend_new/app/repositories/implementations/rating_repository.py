from app.repositories.interfaces.i_rating_repository import IRatingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from app.models.rating import Rating
from app.schemas.rating import RatingFilter
from typing import Optional
from app.core.logging import logger


class RatingRepository(IRatingRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, rating: Rating) -> Optional[Rating]:
        try:
            self.session.add(rating)
            await self.session.commit()
            await self.session.refresh(rating)
            return rating
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(self, filters: Optional[RatingFilter]) -> Optional[list[Rating]]:
        try:
            query = select(Rating)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            ratings = result.scalars().all()
            return ratings if ratings else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Rating]:
        try:
            rating = await self.session.get(Rating, id)
            return rating if rating else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            rating = await self.session.get(Rating, id)

            if not rating:
                return False

            await self.session.delete(rating)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[RatingFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Rating)

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

    def __get_conditions(filters: RatingFilter) -> Optional[list]:
        conditions = []

        if filters.timestamp_after:
            conditions.append(Rating.timestamp >= filters.timestamp_after)
        if filters.timestamp_before:
            conditions.append(Rating.timestamp <= filters.timestamp_before)
        if filters.session_type:
            conditions.append(Rating.session_type == filters.session_type)
        if filters.subject_id:
            conditions.append(Rating.subject_id == filters.subject_id)
        if filters.programme_id:
            conditions.append(Rating.programme_id == filters.programme_id)
        if filters.professor_id:
            conditions.append(Rating.professor_id == filters.professor_id)
        if filters.faculty_id:
            conditions.append(Rating.faculty_id == filters.faculty_id)
        if filters.room_id:
            conditions.append(Rating.room_id == filters.room_id)

        return conditions if conditions else None
        # new_rating = Rating(
        #     rating_clarity=rating.rating_clarity,
        #     rating_interactivity=rating.rating_interactivity,
        #     rating_relevance=rating.rating_relevance,
        #     rating_comprehension=rating.rating_comprehension,
        #     rating_overall=rating.rating_overall,
        #     timestamp=rating.timestamp,
        #     session_type=rating.session_type,
        #     subject_id=rating.subject_id,
        #     programme_id=rating.programme_id,
        #     room_id=rating.room_id,
        #     professor_id=rating.professor_id,
        #     faculty_id=rating.faculty_id,
        # )
