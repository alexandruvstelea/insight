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
from .service import room_to_out, id_to_building


class RoomOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_rooms(self) -> List[RoomOut]:
        try:
            query = select(Room).options(joinedload(Room.building))
            result = await self.session.execute(query)
            rooms = result.scalars().unique().all()
            if rooms:
                return sorted(list(rooms), key=lambda x: x.name)
            raise HTTPException(status_code=404, detail="No rooms found.")
        except Exception as e:
            raise e

    async def get_room_by_id(self, id: int) -> RoomOut:
        room = await self.session.get(Room, id)
        try:
            if room:
                return room_to_out(room)
            raise HTTPException(status_code=404, detail=f"No room with id={id}.")
        except Exception as e:
            raise e

    async def add_room(self, room_data: RoomIn) -> RoomOut:
        try:
            new_room = Room(
                name=room_data.name,
                building_id=room_data.building_id,
            )
            new_room.building = await id_to_building(
                self.session, room_data.building_id
            )
            self.session.add(new_room)
            await self.session.commit()
            await self.session.refresh(new_room)
            return room_to_out(new_room)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_room(self, id: int, new_room_data: RoomIn) -> RoomOut:
        try:
            room = await self.session.get(Room, id)
            if room:
                room.name = new_room_data.name
                if new_room_data.building_id:
                    room.building_id = new_room_data.building_id
                    room.building = await id_to_building(
                        self.session, new_room_data.building_id
                    )
                await self.session.commit()
                return room_to_out(room)
            raise HTTPException(status_code=404, detail=f"No room with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_room(self, id: int):
        try:
            room = await self.session.get(Room, id)
            if room:
                await self.session.delete(room)
                await self.session.commit()
                return JSONResponse(f"Room with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No room with id={id}")
        except Exception as e:
            raise e
