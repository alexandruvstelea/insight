from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import Session
from app.schemas.session import SessionFilter
from typing import Optional


class ISessionRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, session: Session) -> Optional[Session]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Session]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Session]:
        pass

    @abstractmethod
    async def update(self, id: int, session: Session) -> Optional[Session]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def __get_conditions(self, filters: SessionFilter) -> Optional[list]:
        pass

    @abstractmethod
    async def __is_session_overlap(self, session: Session):
        pass
