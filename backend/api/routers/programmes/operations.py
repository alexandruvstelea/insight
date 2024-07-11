from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.programme import Programme
from .schemas import ProgrammeOut, ProgrammeIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from ..faculties.utils import id_to_faculty
from ..subjects.utils import ids_to_subjects
from .utils import programme_to_out
import logging

logger = logging.getLogger(__name__)


class ProgrammeOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_programmes(self, faculty_id: int) -> List[ProgrammeOut]:
        try:
            if faculty_id:
                logger.info(
                    f"Retrieving all programmes with faculty ID {faculty_id} from database."
                )
                query = (
                    select(Programme)
                    .options(
                        joinedload(Programme.faculty), joinedload(Programme.subjects)
                    )
                    .where(Programme.faculty_id == faculty_id)
                )
            else:
                logger.info("Retrieving all programmes from database.")
                query = select(Programme).options(
                    joinedload(Programme.faculty), joinedload(Programme.subjects)
                )
            result = await self.session.execute(query)
            programmes = result.scalars().unique().all()
            if programmes:
                logger.info("Succesfully retrieved all programmes from database.")
                return [
                    programme_to_out(programme)
                    for programme in sorted(list(programmes), key=lambda x: x.name)
                ]
            logger.error("No programmes found.")
            raise HTTPException(status_code=404, detail="No programmes found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving programmes:\n{e}"
            )
            raise e

    async def get_programme_by_id(self, id: int) -> ProgrammeOut:
        try:
            logger.info(f"Retrieving programme with ID {id} from database.")
            programme = await self.session.get(Programme, id)
            if programme:
                logger.info(
                    f"Succesfully retrieved programme with ID {id} from database."
                )
                return programme_to_out(programme)
            logger.error(f"No programme with ID {id} found in database.")
            raise HTTPException(status_code=404, detail=f"No programme with id={id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving programme with ID {id}:\n{e}"
            )
            raise e

    async def add_programme(self, programme_data: ProgrammeIn) -> ProgrammeOut:
        try:
            logger.info(f"Adding to database programme {programme_data}.")
            new_programme = Programme(
                name=programme_data.name,
                abbreviation=programme_data.abbreviation.upper(),
                type=programme_data.type,
                faculty_id=programme_data.faculty_id,
                faculty=await id_to_faculty(self.session, programme_data.faculty_id),
                subjects=[],
            )
            if programme_data.subjects:
                new_programme.subjects = await ids_to_subjects(
                    self.session, programme_data.subjects
                )
            self.session.add(new_programme)
            await self.session.commit()
            await self.session.refresh(new_programme)
            logger.info("Succesfully added new programme to database.")
            return programme_to_out(new_programme)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding programme to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding programme to databse:\n{e}"
            )
            raise e

    async def update_programme(
        self, id: int, new_programme_data: ProgrammeIn
    ) -> ProgrammeOut:
        try:
            logger.info(
                f"Updating programme with ID {id} with new data: {new_programme_data}."
            )
            programme = await self.session.get(Programme, id)
            if programme:
                programme.name = new_programme_data.name
                programme.abbreviation = new_programme_data.abbreviation.upper()
                programme.type = new_programme_data.type
                programme.faculty_id = new_programme_data.faculty_id
                programme.faculty = await id_to_faculty(
                    self.session, new_programme_data.faculty_id
                )
                if new_programme_data.subjects:
                    programme.subjects = [
                        ids_to_subjects(subject)
                        for subject in new_programme_data.subjects
                    ]
                else:
                    programme.subjects = []
                await self.session.commit()
                logger.info(f"Succesfully updated programme with ID {id}.")
                return programme_to_out(programme)
            logger.error(f"No programme with ID {id}")
            raise HTTPException(status_code=404, detail=f"No programme with id={id}.")
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while updating programme with ID {id}:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating programme with ID {id}:\n{e}"
            )
            raise e

    async def delete_programme(self, id: int):
        try:
            logger.info(f"Deleting programme with ID {id}.")
            programme = await self.session.get(Programme, id)
            if programme:
                await self.session.delete(programme)
                await self.session.commit()
                logger.info(f"Succesfully deleted programme with ID {id}.")
                return JSONResponse(f"Programme with ID={id} deleted.")
            logger.error(f"No programme with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No programme with id={id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting programme with ID {id}:\n{e}"
            )
            raise e
