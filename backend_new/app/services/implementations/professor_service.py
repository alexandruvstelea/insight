from app.services.interfaces.i_professor_service import IProfessorService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.professor import Professor
from app.schemas.professor import ProfessorIn, ProfessorOut
from typing import Optional
from app.schemas.professor import ProfessorFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ProfessorService(IProfessorService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, professor_data: ProfessorIn) -> Optional[ProfessorOut]:
        try:
            new_professor = Professor(
                first_name=professor_data.first_name,
                last_name=professor_data.last_name,
                gender=professor_data.gender,
            )

            if professor_data.faculties_ids:
                # TODO
                pass

            response = await self.repository.create(new_professor)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while creating new professor.",
                )

            return ProfessorOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new professor.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while creating new professor.",
            )

    async def get_all(
        self, filters: Optional[ProfessorFilter]
    ) -> Optional[list[ProfessorOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(status_code=404, detail="No professors found.")

            return [ProfessorOut.model_validate(professor) for professor in response]

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while retrieving professors.",
            )

    async def get_by_id(self, id: int) -> Optional[ProfessorOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No professor found for ID={id}."
                )

            return ProfessorOut.model_validate(response)

        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while retrieving professor with ID={id}.",
            )

    async def update(
        self, id: int, professor_data: ProfessorIn
    ) -> Optional[ProfessorOut]:
        try:
            new_professor = Professor(
                first_name=professor_data.first_name,
                last_name=professor_data.last_name,
                gender=professor_data.gender,
            )

            if professor_data.faculties_ids:
                # TODO
                pass

            response = await self.repository.update(id, new_professor)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred while updating professor with ID={id}.",
                )

            return ProfessorOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get("code", 500),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating professor with ID={id}.",
                ),
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while updating professor with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=404, detail=f"No professor with ID={id} found."
                )
            return JSONResponse(f"Professor with ID {id} deleted.")
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while deleting professor with ID={id}.",
            )

    async def count(self, filters: Optional[ProfessorFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except RuntimeError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while counting professors.",
            )
