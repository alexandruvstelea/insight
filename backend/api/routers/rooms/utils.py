from ...database.models.room import Room
from .schemas import RoomOut, RoomOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List
from sqlalchemy import select


def room_to_out(room: Room) -> RoomOut:
    from ..buildings.utils import building_to_minimal
    from ..sessions.utils import session_to_minimal

    return RoomOut(
        id=room.id,
        name=room.name,
        building_id=room.building_id,
        building=building_to_minimal(room.building),
        sessions=(
            [session_to_minimal(session) for session in room.sessions]
            if room.sessions
            else []
        ),
    )


def room_to_minimal(room: Room) -> RoomOutMinimal:
    return RoomOutMinimal(id=room.id, name=room.name, building_id=room.building_id)


async def id_to_room(session: AsyncSession, room_id: int) -> Room:
    room = await session.get(Room, room_id)
    if room:
        return room
    raise HTTPException(status_code=404, detail=f"No room with id={room_id}.")


async def ids_to_rooms(session: AsyncSession, room_ids: List[int]) -> List[Room]:
    result = await session.execute(select(Room).where(Room.id.in_(room_ids)))
    rooms = result.scalars().all()
    if len(rooms) != len(room_ids):
        raise HTTPException(
            status_code=404,
            detail=f"One or more rooms not found for IDs {room_ids}",
        )
    return list(rooms)
