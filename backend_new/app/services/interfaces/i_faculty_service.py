from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.faculty_repository import FacultyRepository
from app.schemas.faculty import FacultyIn, FacultyOut, FacultyFilter
from typing import Optional


class IFacultyService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = FacultyRepository(self.session)

    @abstractmethod
    async def create(self, faculty_data: FacultyIn) -> Optional[FacultyOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[FacultyFilter]
    ) -> Optional[list[FacultyOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[FacultyOut]:
        pass

    @abstractmethod
    async def update(self, id: int, faculty_data: FacultyIn) -> Optional[FacultyOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[FacultyFilter]) -> int:
        pass
