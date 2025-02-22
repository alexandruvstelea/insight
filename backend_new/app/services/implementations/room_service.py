from app.services.interfaces.i_room_service import IRoomService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room
from app.schemas.room import RoomIn, RoomOut
from app.repositories.implementations.building_repository import BuildingRepository
from app.repositories.implementations.session_repository import SessionRepository
from typing import Optional
from app.schemas.room import RoomFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
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
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No building found for ID={new_room.building_id}.",
                )

            new_room.faculties_ids = [
                faculty.id for faculty in new_room.building.faculties
            ]

            if room_data.unique_code:
                if self.__validate_unique_code(room_data.unique_code):
                    new_room.unique_code = room_data.unique_code
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The provided unique room code is not valid.",
                    )
            else:
                new_room.unique_code = self.__generate_unique_code()

            if room_data.sessions_ids:
                for ssn_id in room_data.sessions_ids:
                    session = await SessionRepository(self.session).get_by_id(ssn_id)
                    if not session:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No session found for ID={id}.",
                        )
                    new_room.sessions.append(session)

            response = await self.repository.create(new_room)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new room.",
                )

            return RoomOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new room.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new room.",
            )

    async def get_all(self, filters: Optional[RoomFilter]) -> Optional[list[RoomOut]]:
        try:

            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No rooms found."
                )

            return [RoomOut.model_validate(professor) for professor in response]

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving rooms.",
            )

    async def get_by_id(self, id: int) -> Optional[RoomOut]:
        try:

            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No room found for ID={id}.",
                )

            return RoomOut.model_validate(response)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No building found for ID={new_room.building_id}.",
                )

            new_room.faculties_ids = [
                faculty.id for faculty in new_room.building.faculties
            ]

            if room_data.unique_code:
                if self.__validate_unique_code(room_data.unique_code):
                    new_room.unique_code = room_data.unique_code
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The provided unique room code is not valid.",
                    )
            else:
                new_room.unique_code = self.__generate_unique_code()

            if room_data.sessions_ids:
                for ssn_id in room_data.sessions_ids:
                    session = await SessionRepository(self.session).get_by_id(ssn_id)
                    if not session:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No session found for ID={id}.",
                        )
                    new_room.sessions.append(session)

            response = await self.repository.update(id, new_room)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating room with ID={id}.",
                )

            return RoomOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating room with ID={id}.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating room with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:

            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No room with ID={id} found.",
                )
            return JSONResponse(f"Room with ID {id} deleted.")

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting room with ID={id}.",
            )

    async def count(self, filters: Optional[RoomFilter]):
        try:

            count = await self.repository.count(filters)
            return count

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting rooms.",
            )

    def __generate_unique_code(self) -> str:
        random_part = "".join(choices(ascii_letters + digits, k=6))
        return random_part + "=="

    def __validate_unique_code(self, code: str) -> bool:
        if len(code) != 8:
            return False
        if code[-2:] != "==":
            return False
        if not code[:6].isalnum():
            return False
        return True
