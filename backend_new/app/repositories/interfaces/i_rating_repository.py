from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.rating import Rating
from app.schemas.rating import RatingFilter
from typing import Optional


class IRatingRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, rating: Rating) -> Optional[Rating]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Rating]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Rating]:
        pass

    @abstractmethod
    async def update(self, id: int, rating: Rating) -> Optional[Rating]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def _get_conditions(self, filters: RatingFilter) -> Optional[list]:
        pass
