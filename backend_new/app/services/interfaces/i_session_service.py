from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.session_repository import SessionRepository
from app.schemas.session import SessionIn, SessionOut, SessionFilter
from typing import Optional


class ISessionService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SessionRepository(self.session)

    @abstractmethod
    async def create(self, session_data: SessionIn) -> Optional[SessionOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[SessionFilter]
    ) -> Optional[list[SessionOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[SessionOut]:
        pass

    @abstractmethod
    async def update(self, id: int, session_data: SessionIn) -> Optional[SessionOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[SessionFilter]):
        pass
