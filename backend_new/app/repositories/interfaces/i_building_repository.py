from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.building import Building
from typing import Optional


class IBuildingRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, building: Building) -> Optional[Building]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Building]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Building]:
        pass

    @abstractmethod
    async def update(self, id: int, building: Building) -> Optional[Building]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
