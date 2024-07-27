from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.room import Room
from .schemas import RoomOut, RoomIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import room_to_out
from ..buildings.utils import id_to_building
from ..sessions.utils import ids_to_sessions
import logging

logger = logging.getLogger(__name__)


class RoomOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rooms(self, faculty_id: int) -> List[RoomOut]:
        try:
            logger.info(
                f"Retrieving all rooms with faculty ID {faculty_id} from database."
            )
            if faculty_id:
                query = (
                    select(Room)
                    .options(joinedload(Room.building))
                    .where(Room.faculties_ids.contains([faculty_id]))
                )
            else:
                logger.info("Retrieving all rooms from database.")
                query = select(Room).options(joinedload(Room.building))
            result = await self.session.execute(query)
            rooms = result.scalars().unique().all()
            if rooms:
                logger.info("Succesfully retrieved all rooms from database.")
                return [
                    room_to_out(room)
                    for room in sorted(list(rooms), key=lambda x: x.name)
                ]
            logger.error("No rooms found.")
            raise HTTPException(status_code=404, detail="No rooms found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving rooms:\n{e}"
            )
            raise e

    async def get_room_by_id(self, id: int) -> RoomOut:
        try:
            logger.info(f"Retrieving room with ID {id} from database.")
            room = await self.session.get(Room, id)
            if room:
                logger.info(f"Succesfully retrieved room with ID {id} from database.")
                return room_to_out(room)
            logger.error(f"No room with ID {id} found in database.")
            raise HTTPException(status_code=404, detail=f"No room with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving room with ID {id}:\n{e}"
            )
            raise e

    async def add_room(self, room_data: RoomIn) -> RoomOut:
        try:
            logger.info(f"Adding to database room {room_data}.")
            new_room = Room(
                name=room_data.name.upper(),
                building_id=room_data.building_id,
            )
            new_room.building = await id_to_building(
                self.session, room_data.building_id
            )
            new_room.faculties_ids = [
                faculty.id for faculty in new_room.building.faculties
            ]
            if room_data.sessions:
                new_room.sessions = await ids_to_sessions(
                    self.session, room_data.sessions
                )
            self.session.add(new_room)
            await self.session.commit()
            await self.session.refresh(new_room)
            logger.info("Succesfully added new room to database.")
            return room_to_out(new_room)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding room to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding room to databse:\n{e}"
            )
            raise e

    async def update_room(self, id: int, new_room_data: RoomIn) -> RoomOut:
        try:
            logger.info(f"Updating room with ID {id} with new data: {new_room_data}.")
            room = await self.session.get(Room, id)
            if room:
                room.name = new_room_data.name.upper()
                if new_room_data.building_id:
                    room.building_id = new_room_data.building_id
                    room.building = await id_to_building(
                        self.session, new_room_data.building_id
                    )
                    room.faculties_ids = [
                        faculty.id for faculty in room.building.faculties
                    ]
                if new_room_data.sessions:
                    room.sessions = await ids_to_sessions(
                        self.session, new_room_data.sessions
                    )
                await self.session.commit()
                logger.info(f"Succesfully updated room with ID {id}.")
                return room_to_out(room)
            logger.error(f"No room with ID {id}")
            raise HTTPException(status_code=404, detail=f"No room with ID {id}.")
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while updating room with ID {id}:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating room with ID {id}:\n{e}"
            )
            raise e

    async def delete_room(self, id: int):
        try:
            logger.info(f"Deleting room with ID {id}.")
            room = await self.session.get(Room, id)
            if room:
                await self.session.delete(room)
                await self.session.commit()
                logger.info(f"Succesfully deleted room with ID {id}.")
                return JSONResponse(f"Room with ID={id} deleted.")
            logger.error(f"No room with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No room with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting room with ID {id}:\n{e}"
            )
            raise e
