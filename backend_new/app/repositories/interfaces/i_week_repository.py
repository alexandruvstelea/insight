from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.week import Week
from typing import Optional


class IWeekRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    @staticmethod
    async def create(self, week: Week) -> Optional[Week]:
        pass

    @abstractmethod
    @staticmethod
    async def get_all(self, **filters) -> Optional[list[Week]]:
        pass

    @abstractmethod
    @staticmethod
    async def get_by_id(self) -> Optional[Week]:
        pass

    @abstractmethod
    @staticmethod
    async def update(self, id: int, week: Week) -> Optional[Week]:
        pass

    @abstractmethod
    @staticmethod
    async def delete(self, id: int) -> bool:
        pass
