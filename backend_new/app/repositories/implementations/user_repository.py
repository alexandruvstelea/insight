from app.repositories.interfaces.i_user_repository import IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserFilter
from typing import Optional
from app.core.logging import logger


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user: User) -> Optional[User]:
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(self, filters: Optional[UserFilter]) -> Optional[list[User]]:
        try:
            query = select(User)

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            users = result.scalars().all()

            return users if users else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[User]:
        try:
            user = await self.session.get(User, id)
            return user if user else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_user: User) -> Optional[User]:
        try:
            user = await self.session.get(User, id)

            if not user:
                return None

            user.email = new_user.email
            user.password = new_user.password
            user.role = new_user.role

            await self.session.commit()

            return user
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            user = await self.session.get(User, id)

            if not user:
                return False

            await self.session.delete(user)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[UserFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(User)

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def _get_conditions(filters: UserFilter) -> Optional[list]:
        conditions = []

        if filters.email:
            conditions.append(User.email == filters.email)
        if filters.role:
            conditions.append(User.role == filters.role)
        if filters.professor_id:
            conditions.append(User.professor_id == filters.professor_id)

        return conditions if conditions else None
        # new_user = User(
        #     email=user.email,
        #     password=user.password,
        #     role=user.role,
        # )
