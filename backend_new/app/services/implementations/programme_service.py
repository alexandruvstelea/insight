from app.services.interfaces.i_programme_service import IProgrammeService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.programme import Programme
from app.schemas.programme import ProgrammeIn, ProgrammeOut
from typing import Optional
from app.schemas.programme import ProgrammeFilter
from app.repositories.implementations.faculty_repository import FacultyRepository
from app.repositories.implementations.subject_repository import SubjectRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ProgrammeService(IProgrammeService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, programme_data: ProgrammeIn) -> Optional[ProgrammeOut]:
        try:
            new_programme = Programme(
                name=programme_data.name,
                abbreviation=programme_data.abbreviation.upper(),
                type=programme_data.type,
                faculty_id=programme_data.faculty_id,
            )

            if programme_data.faculty_id:
                new_programme.faculty = await FacultyRepository(self.session).get_by_id(
                    programme_data.faculty_id
                )
                if not new_programme.faculty:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No faculty found for ID={programme_data.faculty_id}.",
                    )

            if programme_data.subjects_ids:
                for id in programme_data.subjects_ids:
                    subject = await SubjectRepository(self.session).get_by_id(id)
                    if not subject:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No subject found for ID={id}.",
                        )
                    new_programme.subjects.append(subject)

            response = await self.repository.create(new_programme)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new programme.",
                )

            return ProgrammeOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new programme.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new programme.",
            )

    async def get_all(
        self, filters: Optional[ProgrammeFilter]
    ) -> Optional[list[ProgrammeOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No programmes found."
                )

            return [ProgrammeOut.model_validate(programme) for programme in response]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while retrieving programmes.",
            )

    async def get_by_id(self, id: int) -> Optional[ProgrammeOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No programme found for ID={id}.",
                )

            return ProgrammeOut.model_validate(response)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving programme with ID={id}.",
            )

    async def update(
        self, id: int, programme_data: ProgrammeIn
    ) -> Optional[ProgrammeOut]:
        try:
            new_programme = Programme(
                name=programme_data.name,
                abbreviation=programme_data.abbreviation.upper(),
                type=programme_data.type,
                faculty_id=programme_data.faculty_id,
            )

            if programme_data.faculty_id:
                new_programme.faculty = await FacultyRepository(self.session).get_by_id(
                    programme_data.faculty_id
                )
                if not new_programme.faculty:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No faculty found for ID={programme_data.faculty_id}.",
                    )

            if programme_data.subjects_ids:
                for id in programme_data.subjects_ids:
                    subject = await SubjectRepository(self.session).get_by_id(id)
                if not subject:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No subject found for ID={id}.",
                    )
                new_programme.subjects.append(subject)

            response = await self.repository.update(id, new_programme)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating programme with ID={id}.",
                )

            return ProgrammeOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating programme with ID={id}.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating programme with ID={id}.",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No programme with ID={id} found.",
                )
            return JSONResponse(f"Programme with ID {id} deleted.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting programme with ID={id}.",
            )

    async def count(self, filters: Optional[ProgrammeFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting programmes.",
            )
