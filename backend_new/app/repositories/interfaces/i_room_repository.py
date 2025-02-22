from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room
from app.schemas.room import RoomFilter
from typing import Optional


class IRoomRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, room: Room) -> Optional[Room]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Room]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Room]:
        pass

    @abstractmethod
    async def update(self, id: int, room: Room) -> Optional[Room]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def _get_conditions(self, filters: RoomFilter) -> Optional[list]:
        pass
