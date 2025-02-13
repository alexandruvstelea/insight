from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.programme_repository import ProgrammeRepository
from app.schemas.programme import ProgrammeIn, ProgrammeOut, ProgrammeFilter
from typing import Optional


class IProgrammeService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProgrammeRepository(self.session)

    @abstractmethod
    async def create(self, programme_data: ProgrammeIn) -> Optional[ProgrammeOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[ProgrammeFilter]
    ) -> Optional[list[ProgrammeOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[ProgrammeOut]:
        pass

    @abstractmethod
    async def update(
        self, id: int, programme_data: ProgrammeIn
    ) -> Optional[ProgrammeOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[ProgrammeFilter]):
        pass
