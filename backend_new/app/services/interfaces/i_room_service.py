from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.room_repository import RoomRepository
from app.schemas.room import RoomIn, RoomOut, RoomFilter
from typing import Optional


class IRoomService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = RoomRepository(self.session)

    @abstractmethod
    async def create(self, room_data: RoomIn) -> Optional[RoomOut]:
        pass

    @abstractmethod
    async def get_all(self, filters: Optional[RoomFilter]) -> Optional[list[RoomOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[RoomOut]:
        pass

    @abstractmethod
    async def update(self, id: int, room_data: RoomIn) -> Optional[RoomOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[RoomFilter]):
        pass

    @abstractmethod
    def __generate_unique_code(self) -> str:
        pass

    @abstractmethod
    def __validate_unique_code(self, code: str) -> bool:
        pass
