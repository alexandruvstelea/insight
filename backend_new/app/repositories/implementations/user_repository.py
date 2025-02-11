from app.repositories.interfaces.i_user_repository import IUserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from app.models.user import User
from app.schemas.user import UserFilter
from typing import Optional
from app.core.logging import logger


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user: User) -> Optional[User]:
        new_user = User(
            email=user.email,
            password=user.password,
            role=user.role,
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_all(self, filters: Optional[UserFilter]) -> Optional[list[User]]:
        conditions = []

        if filters.email:
            conditions.append(User.email == filters.email)
        if filters.role:
            conditions.append(User.role == filters.role)
        if filters.professor_id:
            conditions.append(User.professor_id == filters.professor_id)

        query = select(User)
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        users = result.scalars().all()

        return users if users else None

    async def get_by_id(self, id: int) -> Optional[User]:
        user = await self.session.get(User, id)
        return user if user else None

    async def update(self, id: int, new_user: User) -> Optional[User]:
        user = await self.session.get(User, id)

        if not user:
            return None

        user.email = new_user.email
        user.password = new_user.password
        user.role = new_user.role

        await self.session.commit()

        return user

    async def delete(self, id: int) -> bool:
        user = await self.session.get(User, id)

        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()

        return True
