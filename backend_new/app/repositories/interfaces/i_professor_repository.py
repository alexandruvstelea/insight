from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.professor import Professor
from typing import Optional


class IProfessorRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, professor: Professor) -> Optional[Professor]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Professor]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Professor]:
        pass

    @abstractmethod
    async def update(self, id: int, professor: Professor) -> Optional[Professor]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
