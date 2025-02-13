from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.programme import Programme
from app.schemas.programme import ProgrammeFilter
from typing import Optional


class IProgrammeRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, programme: Programme) -> Optional[Programme]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Programme]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Programme]:
        pass

    @abstractmethod
    async def update(self, id: int, programme: Programme) -> Optional[Programme]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def __get_conditions(filters: ProgrammeFilter) -> Optional[list]:
        pass
