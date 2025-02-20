from app.services.interfaces.i_room_service import IRoomService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room
from app.schemas.room import RoomIn, RoomOut
from app.repositories.implementations.building_repository import BuildingRepository
from typing import Optional
from app.schemas.room import RoomFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger
from random import choices
from string import ascii_letters, digits


class RoomService(IRoomService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, room_data: RoomIn) -> Optional[RoomOut]:
        try:
            new_room = Room(
                name=room_data.name.upper(),
                building_id=room_data.building_id,
            )

            new_room.building = await BuildingRepository(self.session).get_by_id(
                room_data.building_id
            )

            if not new_room.building:
                raise HTTPException(
                    status_code=400,
                    detail=f"No building found for ID={new_room.building_id}.",
                )

            new_room.faculties_ids = [
                faculty.id for faculty in new_room.building.faculties
            ]

            if room_data.unique_code:
                if self._validate_unique_code(room_data.unique_code):
                    new_room.unique_code = room_data.unique_code
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="The provided unique room code is not valid.",
                    )
            else:
                new_room.unique_code = self._generate_unique_code()

            if room_data.sessions_ids:
                # TODO
                pass

            response = await self.repository.create(new_room)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while creating new room.",
                )

            return RoomOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new room.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating new room.",
            )

    async def get_all(self, filters: Optional[RoomFilter]) -> Optional[list[RoomOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(status_code=404, detail="No rooms found.")

            return [RoomOut.model_validate(professor) for professor in response]

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving rooms.",
            )

    async def get_by_id(self, id: int) -> Optional[RoomOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No room found for ID={id}."
                )

            return RoomOut.model_validate(response)

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving room with ID={id}.",
            )

    async def update(self, id: int, room_data: RoomIn) -> Optional[RoomOut]:
        try:
            new_room = Room(
                name=room_data.name.upper(),
                building_id=room_data.building_id,
            )

            new_room.building = await BuildingRepository(self.session).get_by_id(
                room_data.building_id
            )

            if not new_room.building:
                raise HTTPException(
                    status_code=400,
                    detail=f"No building found for ID={new_room.building_id}.",
                )

            new_room.faculties_ids = [
                faculty.id for faculty in new_room.building.faculties
            ]

            if room_data.unique_code:
                if self._validate_unique_code(room_data.unique_code):
                    new_room.unique_code = room_data.unique_code
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="The provided unique room code is not valid.",
                    )
            else:
                new_room.unique_code = self._generate_unique_code()

            if room_data.sessions_ids:
                # TODO
                pass

            response = await self.repository.update(id, new_room)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred while updating room with ID={id}.",
                )

            return RoomOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating room with ID={id}.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while updating room with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No room with ID={id} found."
                )
            return JSONResponse(f"Room with ID {id} deleted.")
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while deleting room with ID={id}.",
            )

    async def count(self, filters: Optional[RoomFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while counting rooms.",
            )

    def _generate_unique_code(self) -> str:
        random_part = "".join(choices(ascii_letters + digits, k=6))
        return random_part + "=="

    def _validate_unique_code(self, code: str) -> bool:
        if len(code) != 8:
            return False
        if code[-2:] != "==":
            return False
        if not code[:6].isalnum():
            return False
        return True
