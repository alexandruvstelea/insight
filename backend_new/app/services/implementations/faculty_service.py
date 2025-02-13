from app.services.interfaces.i_faculty_service import IFacultyService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyIn, FacultyOut
from typing import Optional
from app.schemas.faculty import FacultyFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
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
                # TODO
                pass

            if faculty_data.programmes_ids:
                # TODO
                pass

            if faculty_data.programmes_ids:
                # TODO
                pass

            response = await self.repository.create(new_faculty)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while creating new faculty.",
                )

            return FacultyOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new faculty.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating new faculty.",
            )

    async def get_all(
        self, filters: Optional[FacultyFilter]
    ) -> Optional[list[FacultyOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(status_code=404, detail="No faculties found.")

            return [FacultyOut.model_validate(faculty) for faculty in response]

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving faculties.",
            )

    async def get_by_id(self, id: int) -> Optional[FacultyOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No faculty found for ID={id}."
                )

            return FacultyOut.model_validate(response)

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving faculty with ID={id}.",
            )

    async def update(self, id: int, faculty_data: FacultyIn) -> Optional[FacultyOut]:
        try:
            new_faculty = Faculty(
                name=faculty_data.name,
                abbreviation=faculty_data.abbreviation.upper(),
            )

            if faculty_data.buildings_ids:
                # TODO
                pass

            if faculty_data.programmes_ids:
                # TODO
                pass

            if faculty_data.programmes_ids:
                # TODO
                pass

            response = await self.repository.update(id, new_faculty)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred while updating faculty with ID={id}.",
                )

            return FacultyOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating faculty with ID={id}.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while updating faculty with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No faculty with ID={id} found."
                )
            return JSONResponse(f"Faculty with ID {id} deleted.")
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while deleting faculty with ID={id}.",
            )

    async def count(self, filters: Optional[FacultyFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while counting faculties.",
            )
