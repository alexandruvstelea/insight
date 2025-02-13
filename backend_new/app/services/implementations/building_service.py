from app.services.interfaces.i_building_service import IBuildingService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.building import Building
from app.schemas.building import BuildingIn, BuildingOut
from typing import Optional
from app.schemas.building import BuildingFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
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
                # TODO Implement this
                pass

            if building_data.rooms_ids:
                # TODO Implement this
                pass

            response = await self.repository.create(new_building)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while creating new building.",
                )

            return BuildingOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new building.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating new building.",
            )

    async def get_all(
        self, filters: Optional[BuildingFilter] = None
    ) -> Optional[list[BuildingOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(status_code=404, detail="No buildings found.")

            return [BuildingOut.model_validate(building) for building in response]

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving buildings.",
            )

    async def get_by_id(self, id: int) -> Optional[BuildingOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No building found for ID={id}."
                )

            return BuildingOut.model_validate(response)

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
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
                # TODO Implement this
                pass

            if building_data.rooms_ids:
                # TODO Implement this
                pass

            response = await self.repository.update(id, new_building)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred while updating building with ID={id}.",
                )

            return BuildingOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating building with ID={id}.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while updating building with ID={id}.",
            )

    async def delete(self, id: int) -> JSONResponse:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No building with ID={id} found."
                )
            return JSONResponse(f"Building with ID {id} deleted.")
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while deleting building with ID={id}.",
            )

    async def count(self, filters: Optional[BuildingFilter] = None) -> Optional[int]:
        try:
            count = await self.repository.count(filters)
            return count
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while counting buildings.",
            )
