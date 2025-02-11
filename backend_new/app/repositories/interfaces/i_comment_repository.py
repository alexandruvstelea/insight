from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment
from typing import Optional


class ICommentRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, comment: Comment) -> Optional[Comment]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Comment]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Comment]:
        pass

    @abstractmethod
    async def update(self, id: int, comment: Comment) -> Optional[Comment]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
