from app.repositories.interfaces.i_room_repository import IRoomRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.models.room import Room
from app.schemas.room import RoomFilter
from typing import Optional
from app.core.logging import logger


class RoomRepository(IRoomRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, room: Room) -> Optional[Room]:
        try:
            self.session.add(room)
            await self.session.commit()
            await self.session.refresh(room)
            return room
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(self, filters: Optional[RoomFilter]) -> Optional[list[Room]]:
        try:
            query = select(Room).options(joinedload(Room.building))

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            rooms = result.scalars().unique().all()

            return rooms if rooms else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Room]:
        try:
            room = await self.session.get(Room, id)
            return room if room else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_room: Room) -> Optional[Room]:
        try:
            room = await self.session.get(Room, id)

            if not room:
                return None

            room.name = new_room.name.upper()
            room.unique_code = new_room.unique_code
            room.building_id = new_room.building_id
            room.building = new_room.building
            room.faculties_ids = new_room.faculties_ids
            room.sessions = new_room.sessions

            await self.session.commit()

            return room
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            room = await self.session.get(Room, id)

            if not room:
                return False

            await self.session.delete(room)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[RoomFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Room)

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

    def _get_conditions(self, filters: RoomFilter) -> Optional[list]:
        conditions = []

        if filters.name:
            conditions.append(Room.name == filters.name)
        if filters.unique_code:
            conditions.append(Room.unique_code == filters.unique_code)

        return conditions if conditions else None
