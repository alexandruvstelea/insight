from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subject import Subject
from app.schemas.subject import SubjectFilter
from typing import Optional


class ISubjectRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, subject: Subject) -> Optional[Subject]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Subject]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Subject]:
        pass

    @abstractmethod
    async def update(self, id: int, subject: Subject) -> Optional[Subject]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def __get_conditions(self, filters: SubjectFilter) -> Optional[list]:
        pass
