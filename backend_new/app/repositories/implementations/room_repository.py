from app.repositories.interfaces.i_room_repository import IRoomRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from sqlalchemy.orm import joinedload
from app.models.room import Room
from app.schemas.room import RoomFilter
from typing import Optional
from app.core.logging import logger


class RoomRepository(IRoomRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, room: Room) -> Optional[Room]:
        new_room = Room(
            name=room.name.upper(),
            unique_code=room.unique_code,
            building_id=room.building_id,
            building=room.building,
            faculties_ids=room.faculties_ids,
            sessions=room.sessions,
        )

        self.session.add(new_room)
        await self.session.commit()
        await self.session.refresh(new_room)

        return new_room

    async def get_all(self, filters: Optional[RoomFilter]) -> Optional[list[Room]]:
        conditions = []

        if filters.name:
            conditions.append(Room.name == filters.name)
        if filters.unique_code:
            conditions.append(Room.unique_code == filters.unique_code)

        query = select(Room).options(joinedload(Room.building))
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        rooms = result.scalars().all()

        return rooms if rooms else None

    async def get_by_id(self, id: int) -> Optional[Room]:
        room = await self.session.get(Room, id)
        return room if room else None

    async def update(self, id: int, new_room: Room) -> Optional[Room]:
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

    async def delete(self, id: int) -> bool:
        room = await self.session.get(Room, id)

        if not room:
            return False

        await self.session.delete(room)
        await self.session.commit()

        return True
