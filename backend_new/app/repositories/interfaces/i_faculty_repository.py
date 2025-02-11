from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.faculty import Faculty
from typing import Optional


class IFacultyRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, faculty: Faculty) -> Optional[Faculty]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Faculty]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Faculty]:
        pass

    @abstractmethod
    async def update(self, id: int, faculty: Faculty) -> Optional[Faculty]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
