from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.week_repository import WeekRepository
from app.schemas.week import WeekIn, WeekOut, WeekFilter
from typing import Optional


class IWeekService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = WeekRepository(self.session)

    @abstractmethod
    async def create(self, week_data: WeekIn) -> Optional[WeekOut]:
        pass

    @abstractmethod
    async def get_all(self, filters: Optional[WeekFilter]) -> Optional[list[WeekOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[WeekOut]:
        pass

    @abstractmethod
    async def update(self, id: int, week_data: WeekIn) -> Optional[WeekOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[WeekFilter]):
        pass
