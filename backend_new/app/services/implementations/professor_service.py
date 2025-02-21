from app.services.interfaces.i_professor_service import IProfessorService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.professor import Professor
from app.schemas.professor import ProfessorIn, ProfessorOut
from typing import Optional
from app.schemas.professor import ProfessorFilter
from app.repositories.implementations.faculty_repository import FacultyRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
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
                for fac_id in professor_data.faculties_ids:
                    faculty = await FacultyRepository(self.session).get_by_id(fac_id)
                    if not faculty:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No faculty found for ID={id}.",
                        )
                    new_professor.faculties.append(faculty)

            response = await self.repository.create(new_professor)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new professor.",
                )

            return ProfessorOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new professor.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new professor.",
            )

    async def get_all(
        self, filters: Optional[ProfessorFilter]
    ) -> Optional[list[ProfessorOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No professors found."
                )

            return [ProfessorOut.model_validate(professor) for professor in response]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while retrieving professors.",
            )

    async def get_by_id(self, id: int) -> Optional[ProfessorOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No professor found for ID={id}.",
                )

            return ProfessorOut.model_validate(response)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
                for fac_id in professor_data.faculties_ids:
                    faculty = await FacultyRepository(self.session).get_by_id(fac_id)
                    if not faculty:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No faculty found for ID={id}.",
                        )
                    new_professor.faculties.append(faculty)

            response = await self.repository.update(id, new_professor)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating professor with ID={id}.",
                )

            return ProfessorOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating professor with ID={id}.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating professor with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No professor with ID={id} found.",
                )
            return JSONResponse(f"Professor with ID {id} deleted.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting professor with ID={id}.",
            )

    async def count(self, filters: Optional[ProfessorFilter]) -> int:
        try:
            count = await self.repository.count(filters)
            return count
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting professors.",
            )
