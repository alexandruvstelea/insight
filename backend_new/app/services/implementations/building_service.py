from app.services.interfaces.i_building_service import IBuildingService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.building import Building
from app.schemas.building import BuildingIn, BuildingOut
from typing import Optional
from app.schemas.building import BuildingFilter
from app.repositories.implementations.faculty_repository import FacultyRepository
from app.repositories.implementations.room_repository import RoomRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from math import radians, atan2, sqrt, cos, sin
from app.core.logging import logger


class BuildingService(IBuildingService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, building_data: BuildingIn) -> Optional[BuildingOut]:
        try:

            new_building = Building(
                name=building_data.name,
                latitude=building_data.latitude,
                longitude=building_data.longitude,
            )

            if building_data.faculties_ids:
                for fac_id in building_data.faculties_ids:
                    faculty = await FacultyRepository(self.session).get_by_id(fac_id)
                    if not faculty:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No faculty found for ID={id}.",
                        )
                    new_building.faculties.append(faculty)

            if building_data.rooms_ids:
                for room_id in building_data.rooms_ids:
                    room = await RoomRepository(self.session).get_by_id(room_id)
                    if not room:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No room found for ID={id}.",
                        )
                    new_building.rooms.append(room)

            response = await self.repository.create(new_building)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new building.",
                )

            return BuildingOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new building.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new building.",
            )

    async def get_all(
        self, filters: Optional[BuildingFilter] = None
    ) -> Optional[list[BuildingOut]]:
        try:

            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No buildings found."
                )

            return [BuildingOut.model_validate(building) for building in response]

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving buildings.",
            )

    async def get_by_id(self, id: int) -> Optional[BuildingOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No building found for ID={id}.",
                )

            return BuildingOut.model_validate(response)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving building with ID={id}.",
            )

    async def update(self, id: int, building_data: BuildingIn) -> Optional[Building]:
        try:

            new_building = Building(
                name=building_data.name,
                latitude=building_data.latitude,
                longitude=building_data.longitude,
            )

            if building_data.faculties_ids:
                for fac_id in building_data.faculties_ids:
                    faculty = await FacultyRepository(self.session).get_by_id(fac_id)
                    if not faculty:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No faculty found for ID={id}.",
                        )
                    new_building.faculties.append(faculty)

            if building_data.rooms_ids:
                for room_id in building_data.rooms_ids:
                    room = await RoomRepository(self.session).get_by_id(room_id)
                    if not room:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No room found for ID={id}.",
                        )
                    new_building.rooms.append(room)

            response = await self.repository.update(id, new_building)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating building with ID={id}.",
                )

            return BuildingOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating building with ID={id}.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating building with ID={id}.",
            )

    async def delete(self, id: int) -> JSONResponse:
        try:

            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No building with ID={id} found.",
                )
            return JSONResponse(f"Building with ID {id} deleted.")

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting building with ID={id}.",
            )

    async def count(self, filters: Optional[BuildingFilter] = None) -> int:
        try:

            count = await self.repository.count(filters)
            return count

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting buildings.",
            )

    def get_distance(
        self, rating_location: tuple, building: Building
    ) -> Optional[float]:
        try:

            logger.info("Calculating distance to building from rating distance.")
            R = 6371000
            lat1, lon1 = rating_location
            lat2, lon2 = building.latitude, building.longitude
            lat1_rad, lon1_rad = radians(lat1), radians(lon1)
            lat2_rad, lon2_rad = radians(lat2), radians(lon2)
            delta_lat = lat2_rad - lat1_rad
            delta_lon = lon2_rad - lon1_rad
            a = (
                sin(delta_lat / 2) ** 2
                + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
            )
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            return distance

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while calculating distance:\n{e}"
            )
            raise e
