from sqlalchemy import select
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


class ProfessorOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_professors(self, faculty_id: int) -> List[ProfessorOut]:
        try:
            if faculty_id:
                query = (
                    select(Professor)
                    .options(joinedload(Professor.faculties))
                    .where(Professor.faculties_ids.contains([faculty_id]))
                )
            else:
                query = select(Professor).options(joinedload(Professor.faculties))
            result = await self.session.execute(query)
            professors = result.scalars().unique().all()
            if professors:
                return [
                    professor_to_out(professor)
                    for professor in sorted(professors, key=lambda x: x.last_name)
                ]
            raise HTTPException(status_code=404, detail="No professors found.")
        except Exception as e:
            raise e

    async def get_professor_by_id(self, id: int) -> ProfessorOut:
        professor = await self.session.get(Professor, id)
        try:
            if professor:
                return professor_to_out(professor)
            raise HTTPException(status_code=404, detail=f"No professor with id={id}.")
        except Exception as e:
            raise e

    async def add_professor(self, professor_data: ProfessorIn) -> ProfessorOut:
        try:
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
            return professor_to_out(new_professor)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_professor(
        self, id: int, new_professor_data: ProfessorIn
    ) -> ProfessorOut:
        try:
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
                return professor_to_out(professor)
            raise HTTPException(status_code=404, detail=f"No professor with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_professor(self, id: int):
        try:
            professor = await self.session.get(Professor, id)
            if professor:
                await self.session.delete(professor)
                await self.session.commit()
                return JSONResponse(f"Professor with ID={id} deleted.")
            else:
                raise HTTPException(
                    status_code=404, detail=f"No professor with id={id}."
                )
        except Exception as e:
            raise e
