from app.services.interfaces.i_subject_service import ISubjectService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subject import Subject
from app.schemas.subject import SubjectIn, SubjectOut
from app.repositories.implementations.programme_repository import ProgrammeRepository
from typing import Optional
from app.schemas.subject import SubjectFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class SubjectService(ISubjectService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, subject_data: SubjectIn) -> Optional[SubjectOut]:
        try:

            new_subject = Subject(
                name=subject_data.name,
                abbreviation=subject_data.abbreviation.upper(),
                semester=subject_data.semester,
                course_professor_id=subject_data.course_professor_id,
                laboratory_professor_id=subject_data.laboratory_professor_id,
                seminar_professor_id=subject_data.seminar_professor_id,
                project_professor_id=subject_data.project_professor_id,
            )

            if subject_data.programmes_ids:
                for id in subject_data.programmes_ids:
                    programme = await ProgrammeRepository(self.session).get_by_id(id)
                    if not programme:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No programme found for ID={id}.",
                        )
                    new_subject.programmes.append(programme)

            response = await self.repository.create(new_subject)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new subject.",
                )

            return SubjectOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new subject.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new subject.",
            )

    async def get_all(
        self, filters: Optional[SubjectFilter]
    ) -> Optional[list[SubjectOut]]:
        try:

            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No subjects found."
                )

            return [SubjectOut.model_validate(subject) for subject in response]

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while retrieving subjects.",
            )

    async def get_by_id(self, id: int) -> Optional[SubjectOut]:
        try:

            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No subject found for ID={id}.",
                )

            return SubjectOut.model_validate(response)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving subject with ID={id}.",
            )

    async def update(self, id: int, subject_data: SubjectIn) -> Optional[SubjectOut]:
        try:

            new_subject = Subject(
                name=subject_data.name,
                abbreviation=subject_data.abbreviation.upper(),
                semester=subject_data.semester,
                course_professor_id=subject_data.course_professor_id,
                laboratory_professor_id=subject_data.laboratory_professor_id,
                seminar_professor_id=subject_data.seminar_professor_id,
                project_professor_id=subject_data.project_professor_id,
            )

            if subject_data.programmes_ids:
                for prog_id in subject_data.programmes_ids:
                    programme = await ProgrammeRepository(self.session).get_by_id(
                        prog_id
                    )
                    if not programme:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No programme found for ID={prog_id}.",
                        )
                    new_subject.programmes.append(programme)

            response = await self.repository.update(id, new_subject)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating subject with ID={id}.",
                )

            return SubjectOut.model_validate(response)

        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating subject with ID={id}.",
                ),
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating subject with ID={id}.{e}",
            )

    async def delete(self, id: int) -> bool:
        try:

            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No subject with ID={id} found.",
                )
            return JSONResponse(f"Subject with ID {id} deleted.")

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting subject with ID={id}.",
            )

    async def count(self, filters: Optional[SubjectFilter]):
        try:

            count = await self.repository.count(filters)
            return count

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting subjects.",
            )
