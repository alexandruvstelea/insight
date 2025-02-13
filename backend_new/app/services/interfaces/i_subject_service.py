from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.subject_repository import SubjectRepository
from app.schemas.subject import SubjectIn, SubjectOut, SubjectFilter
from typing import Optional


class ISubjectService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SubjectRepository(self.session)

    @abstractmethod
    async def create(self, subject_data: SubjectIn) -> Optional[SubjectOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[SubjectFilter]
    ) -> Optional[list[SubjectOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[SubjectOut]:
        pass

    @abstractmethod
    async def update(self, id: int, subject_data: SubjectIn) -> Optional[SubjectOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[SubjectFilter]):
        pass
