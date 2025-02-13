from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.user import UserIn, UserOut, UserFilter
from typing import Optional


class IUserService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(self.session)

    @abstractmethod
    async def create(self, user_data: UserIn) -> Optional[UserOut]:
        pass

    @abstractmethod
    async def get_all(self, filters: Optional[UserFilter]) -> Optional[list[UserOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[UserOut]:
        pass

    @abstractmethod
    async def update(self, id: int, user_data: UserIn) -> Optional[UserOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[UserFilter]):
        pass
