from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from typing import Optional


class IUserRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[User]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, id: int, user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
