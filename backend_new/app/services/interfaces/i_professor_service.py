from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.professor_repository import ProfessorRepository
from app.schemas.professor import ProfessorIn, ProfessorOut, ProfessorFilter
from typing import Optional


class IProfessorService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProfessorRepository(self.session)

    @abstractmethod
    async def create(self, professor_data: ProfessorIn) -> Optional[ProfessorOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[ProfessorFilter]
    ) -> Optional[list[ProfessorOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[ProfessorOut]:
        pass

    @abstractmethod
    async def update(
        self, id: int, professor_data: ProfessorIn
    ) -> Optional[ProfessorOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[ProfessorFilter]) -> int:
        pass
