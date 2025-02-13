from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.rating_repository import RatingRepository
from app.schemas.rating import RatingIn, RatingOut, RatingFilter
from typing import Optional


class IRatingService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = RatingRepository(self.session)

    @abstractmethod
    async def create(self, rating_data: RatingIn) -> Optional[RatingOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[RatingFilter]
    ) -> Optional[list[RatingOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RatingOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[RatingFilter]):
        pass
