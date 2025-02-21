from app.repositories.interfaces.i_comment_repository import ICommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from app.models.comment import Comment
from typing import Optional
from app.core.logging import logger
from app.schemas.comment import CommentFilter


class CommentRepository(ICommentRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, comment: Comment) -> Optional[Comment]:
        try:
            self.session.add(comment)
            await self.session.commit()
            await self.session.refresh(comment)
            return comment
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[CommentFilter],
    ) -> Optional[list[Comment]]:
        try:
            query = select(Comment)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)

            result = await self.session.execute(query)
            comments = result.scalars().all()
            return comments if comments else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Comment]:
        try:
            comment = await self.session.get(Comment, id)
            return comment if comment else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_comment: Comment) -> Optional[Comment]:
        try:
            comment = await self.session.get(Comment, id)

            if not comment:
                return None

            comment.text = new_comment.text
            comment.subject_id = new_comment.subject_id
            comment.timestamp = new_comment.timestamp
            comment.programme_id = new_comment.programme_id
            comment.room_id = new_comment.room_id
            comment.professor_id = new_comment.professor_id
            comment.faculty_id = new_comment.faculty_id
            comment.session_type = new_comment.session_type

            await self.session.commit()

            return comment
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            comment = await self.session.get(Comment, id)

            if not comment:
                return False

            await self.session.delete(comment)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[CommentFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Comment)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def __get_conditions(self, filters: CommentFilter) -> Optional[list]:
        conditions = []

        if filters.timestamp_after:
            conditions.append(Comment.timestamp >= filters.timestamp_after)
        if filters.timestamp_before:
            conditions.append(Comment.timestamp <= filters.timestamp_before)
        if filters.session_type:
            conditions.append(Comment.session_type == filters.session_type)

        return conditions if conditions else None

        # new_comment = Comment(
        #     text=comment.text,
        #     subject_id=comment.subject_id,
        #     timestamp=comment.timestamp,
        #     programme_id=comment.programme_id,
        #     room_id=comment.room_id,
        #     professor_id=comment.professor_id,
        #     faculty_id=comment.faculty_id,
        #     session_type=comment.session_type,
        # )
