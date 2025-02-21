from app.services.interfaces.i_faculty_service import IFacultyService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyIn, FacultyOut
from typing import Optional
from app.schemas.faculty import FacultyFilter
from app.repositories.implementations.building_repository import BuildingRepository
from app.repositories.implementations.programme_repository import ProgrammeRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class FacultyService(IFacultyService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, faculty_data: FacultyIn) -> Optional[FacultyOut]:
        try:
            new_faculty = Faculty(
                name=faculty_data.name,
                abbreviation=faculty_data.abbreviation.upper(),
            )

            if faculty_data.buildings_ids:
                for bdg_id in faculty_data.buildings_ids:
                    building = await BuildingRepository(self.session).get_by_id(bdg_id)
                    if not building:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No building found for ID={id}.",
                        )
                    new_faculty.buildings.append(building)

            if faculty_data.programmes_ids:
                for pgm_id in faculty_data.programmes_ids:
                    programme = await ProgrammeRepository(self.session).get_by_id(
                        pgm_id
                    )
                    if not programme:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No programme found for ID={id}.",
                        )
                    new_faculty.programmes.append(programme)

            response = await self.repository.create(new_faculty)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new faculty.",
                )

            return FacultyOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new faculty.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new faculty.",
            )

    async def get_all(
        self, filters: Optional[FacultyFilter]
    ) -> Optional[list[FacultyOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No faculties found."
                )

            return [FacultyOut.model_validate(faculty) for faculty in response]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving faculties.",
            )

    async def get_by_id(self, id: int) -> Optional[FacultyOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No faculty found for ID={id}.",
                )

            return FacultyOut.model_validate(response)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving faculty with ID={id}.",
            )

    async def update(self, id: int, faculty_data: FacultyIn) -> Optional[FacultyOut]:
        try:
            new_faculty = Faculty(
                name=faculty_data.name,
                abbreviation=faculty_data.abbreviation.upper(),
            )

            if faculty_data.buildings_ids:
                for bdg_id in faculty_data.buildings_ids:
                    building = await BuildingRepository(self.session).get_by_id(bdg_id)
                    if not building:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No building found for ID={id}.",
                        )
                    new_faculty.buildings.append(building)

            if faculty_data.programmes_ids:
                for pgm_id in faculty_data.programmes_ids:
                    programme = await ProgrammeRepository(self.session).get_by_id(
                        pgm_id
                    )
                    if not programme:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No programme found for ID={id}.",
                        )
                    new_faculty.programmes.append(programme)

            response = await self.repository.update(id, new_faculty)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating faculty with ID={id}.",
                )

            return FacultyOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating faculty with ID={id}.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating faculty with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No faculty with ID={id} found.",
                )
            return JSONResponse(f"Faculty with ID {id} deleted.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting faculty with ID={id}.",
            )

    async def count(self, filters: Optional[FacultyFilter]) -> int:
        try:
            count = await self.repository.count(filters)
            return count
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting faculties.",
            )
