from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.faculty import Faculty
from .schemas import FacultyOut, FacultyIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import faculty_to_out
from ..buildings.utils import ids_to_buildings
from ..professors.utils import ids_to_professors
from ..programmes.utils import ids_to_programmes


class FacultyOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_faculties(self) -> List[FacultyOut]:
        try:
            query = select(Faculty).options(joinedload(Faculty.buildings))
            result = await self.session.execute(query)
            faculties = result.scalars().unique().all()
            if faculties:
                return [
                    faculty_to_out(faculty)
                    for faculty in sorted(list(faculties), key=lambda x: x.name)
                ]
            raise HTTPException(status_code=404, detail="No faculties found.")
        except Exception as e:
            raise e

    async def get_faculty_by_id(self, id: int) -> FacultyOut:
        faculty = await self.session.get(Faculty, id)
        try:
            if faculty:
                return faculty_to_out(faculty)
            raise HTTPException(status_code=404, detail=f"No faculty with id={id}.")
        except Exception as e:
            raise e

    async def add_faculty(self, faculty_data: FacultyIn) -> FacultyOut:
        try:
            new_faculty = Faculty(
                name=faculty_data.name,
                abbreviation=faculty_data.abbreviation.upper(),
                buildings=[],
                professors=[],
            )
            if faculty_data.buildings:
                new_faculty.buildings = await ids_to_buildings(
                    self.session, faculty_data.buildings
                )
            if faculty_data.professors:
                new_faculty.professors = await ids_to_professors(
                    self.session, faculty_data.professors
                )
            if faculty_data.programmes:
                new_faculty.programmes = await ids_to_programmes(
                    self.session, faculty_data.programmes
                )
            self.session.add(new_faculty)
            await self.session.commit()
            await self.session.refresh(new_faculty)
            return faculty_to_out(new_faculty)
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_faculty(self, id: int, new_faculty_data: FacultyIn) -> FacultyOut:
        try:
            faculty = await self.session.get(Faculty, id)
            if faculty:
                faculty.name = new_faculty_data.name
                faculty.abbreviation = new_faculty_data.abbreviation.upper()
                if new_faculty_data.buildings:
                    faculty.buildings = await ids_to_buildings(
                        self.session, new_faculty_data.buildings
                    )
                else:
                    faculty.buildings = []
                if new_faculty_data.professors:
                    faculty.professors = await ids_to_professors(
                        self.session, new_faculty_data.professors
                    )
                else:
                    faculty.professors = []
                if new_faculty_data.programmes:
                    faculty.programmes = await ids_to_programmes(
                        self.session, new_faculty_data.programmes
                    )
                else:
                    faculty.programmes = []
                await self.session.commit()
                return faculty_to_out(faculty)
            raise HTTPException(status_code=404, detail=f"No faculty with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_faculty(self, id: int):
        try:
            faculty = await self.session.get(Faculty, id)
            if faculty:
                await self.session.delete(faculty)
                await self.session.commit()
                return JSONResponse(f"Faculty with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No faculty with id={id}")
        except Exception as e:
            raise e
