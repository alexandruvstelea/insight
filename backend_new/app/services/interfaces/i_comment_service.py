from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.comment_repository import CommentRepository
from app.schemas.comment import CommentIn, CommentOut, CommentFilter
from typing import Optional


class ICommentService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = CommentRepository(self.session)

    @abstractmethod
    async def create(self, comment_data: CommentIn) -> Optional[CommentOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[CommentFilter]
    ) -> Optional[list[CommentOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[CommentOut]:
        pass

    @abstractmethod
    async def update(self, id: int, comment_data: CommentIn) -> Optional[CommentOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[CommentFilter]):
        pass
