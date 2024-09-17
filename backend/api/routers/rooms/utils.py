from ...database.models.room import Room
from .schemas import RoomOut, RoomOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


def room_to_out(room: Room) -> RoomOut:
    from ..buildings.utils import building_to_minimal
    from ..sessions.utils import session_to_minimal
    if room:
        logger.info(f"Converting room {room.name} to RoomOut format.")
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
    return None

def room_to_minimal(room: Room) -> RoomOutMinimal:
    if room:
        logger.info(f"Converting room {room.name} to RoomOutMinimal format.")
        return RoomOutMinimal(id=room.id, name=room.name, building_id=room.building_id)
    return None

async def id_to_room(session: AsyncSession, room_id: int) -> Room:
    try:
        if room_id:
            logger.info(f"Retrieving room for ID {room_id}.")
            room = await session.get(Room, room_id)
            if room:
                logger.info(f"Retrieved room with ID {room_id}.")
                return room
            logger.error(f"No room with ID {room_id}.")
            raise HTTPException(status_code=404, detail=f"No room with ID {room_id}.")
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving room with ID {room_id}:\n{e}"
        )
        raise e


async def ids_to_rooms(session: AsyncSession, room_ids: List[int]) -> List[Room]:
    try:
        if room_ids:
            logger.info(f"Retrieving rooms with IDs {room_ids}.")
            result = await session.execute(select(Room).where(Room.id.in_(room_ids)))
            rooms = result.scalars().all()
            if len(rooms) != len(room_ids):
                logger.error(f"One or more rooms not found for IDs {room_ids}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"One or more rooms not found for IDs {room_ids}",
                )
            logger.info(f"Retrieved rooms with IDs {room_ids}.")
            return list(rooms)
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while retrieving rooms with IDs {room_ids}:\n{e}"
        )
        raise e
