from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from ...database.models.professor import Professor
from .schemas import ProfessorOut, ProfessorIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from ..faculties.utils import ids_to_faculties
from .utils import professor_to_out
import logging

logger = logging.getLogger(__name__)


class ProfessorOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_professors(self, faculty_id: int) -> List[ProfessorOut]:
        try:
            if faculty_id:
                logger.info(
                    f"Retrieving all professors with faculty ID {faculty_id} from database."
                )
                query = (
                    select(Professor)
                    .options(joinedload(Professor.faculties))
                    .where(Professor.faculties_ids.contains([faculty_id]))
                )
            else:
                logger.info("Retrieving all professors from database.")
                query = select(Professor).options(joinedload(Professor.faculties))
            result = await self.session.execute(query)
            professors = result.scalars().unique().all()
            if professors:
                logger.info("Succesfully retrieved all professors from database.")
                return [
                    professor_to_out(professor)
                    for professor in sorted(professors, key=lambda x: x.last_name)
                ]
            logger.error("No professors found.")
            raise HTTPException(status_code=404, detail="No professors found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving professors:\n{e}"
            )
            raise e

    async def get_professor_by_id(self, id: int) -> ProfessorOut:
        try:
            logger.info(f"Retrieving professor with ID {id} from database.")
            professor = await self.session.get(Professor, id)
            if professor:
                logger.info(
                    f"Succesfully retrieved professor with ID {id} from database."
                )
                return professor_to_out(professor)
            logger.error(f"No professor with ID {id} found in database.")
            raise HTTPException(status_code=404, detail=f"No professor with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving professor with ID {id}:\n{e}"
            )
            raise e

    async def get_professor_by_full_name(
        self, first_name: str, last_name: str
    ) -> ProfessorOut:
        try:
            logger.info(
                f"Retrieving professor with name {last_name} {first_name} from database."
            )
            result = await self.session.execute(
                select(Professor).where(
                    and_(
                    Professor.first_name == first_name,
                    Professor.last_name == last_name
                )
                )
            )
            professor = result.scalars().unique().one_or_none()
            if professor:
                logger.info(
                    f"Succesfully retrieved professor name {last_name} {first_name} from database."
                )
                return professor_to_out(professor)
            logger.error(
                f"No professor name {last_name} {first_name} found in database."
            )
            raise HTTPException(
                status_code=404, detail=f"No professorname {last_name} {first_name}."
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving professor name {last_name} {first_name}:\n{e}"
            )
            raise e

    async def add_professor(self, professor_data: ProfessorIn) -> ProfessorOut:
        try:
            logger.info(f"Adding to database professor {professor_data}.")
            new_professor = Professor(
                first_name=professor_data.first_name,
                last_name=professor_data.last_name,
                gender=professor_data.gender,
                faculties=[],
                courses=[],
                laboratories=[],
                seminars=[],
                projects=[],
            )
            if professor_data.faculties:
                new_professor.faculties = await ids_to_faculties(
                    self.session, professor_data.faculties
                )
                new_professor.faculties_ids = professor_data.faculties
            self.session.add(new_professor)
            await self.session.commit()
            await self.session.refresh(new_professor)
            logger.info("Succesfully added new professor to database.")
            return professor_to_out(new_professor)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding professor to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding professor to databse:\n{e}"
            )
            raise e

    async def update_professor(
        self, id: int, new_professor_data: ProfessorIn
    ) -> ProfessorOut:
        try:
            logger.info(
                f"Updating professor with ID {id} with new data: {new_professor_data}."
            )
            professor = await self.session.get(Professor, id)
            if professor:
                professor.first_name = new_professor_data.first_name
                professor.last_name = new_professor_data.last_name
                professor.gender = new_professor_data.gender
                if new_professor_data.faculties:
                    professor.faculties = await ids_to_faculties(
                        self.session, new_professor_data.faculties
                    )
                    professor.faculties_ids = new_professor_data.faculties
                else:
                    professor.faculties = []
                    professor.faculties_ids = []
                await self.session.commit()
                logger.info(f"Succesfully updated professor with ID {id}.")
                return professor_to_out(professor)
            logger.error(f"No professor with ID {id}")
            raise HTTPException(status_code=404, detail=f"No professor with ID {id}.")
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while updating professor with ID {id}:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating professor with ID {id}:\n{e}"
            )
            raise e

    async def delete_professor(self, id: int):
        try:
            logger.info(f"Deleting professor with ID {id}.")
            professor = await self.session.get(Professor, id)
            if professor:
                await self.session.delete(professor)
                await self.session.commit()
                logger.info(f"Succesfully deleted professor with ID {id}.")
                return JSONResponse(f"Professor with ID={id} deleted.")
            logger.error(f"No professor with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No professor with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting professor with ID {id}:\n{e}"
            )
            raise e

    async def get_entities_count(self, faculty_id: int) -> int:
        try:
            logger.info(f"Counting professors in faculty with ID {faculty_id}.")
            count_query = (
                select(func.count())
                .select_from(Professor)
                .where(Professor.faculties_ids.contains([faculty_id]))
            )
            result = await self.session.execute(count_query)
            count = result.scalar()
            logger.info(
                f"There are {count} professors in the faculty with ID {faculty_id}."
            )
            return count
        except Exception as e:
            logger.error(f"An error occurred while counting professors:\n{e}")
            raise HTTPException(
                status_code=500, detail="Could not retrieve professor count"
            )
