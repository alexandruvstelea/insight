from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.building import Building
from ...database.models.faculty import Faculty
from .schemas import FacultyOut, FacultyIn
from ..buildings.schemas import BuildingOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error


class FacultyService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_faculties(self) -> List[FacultyOut]:
        try:
            query = select(Faculty).options(joinedload(Faculty.buildings))
            result = await self.session.execute(query)
            if result:
                faculties = result.scalars().unique()
                return sorted(list(faculties), key=lambda x: x.name)
            raise HTTPException(status_code=404, detail="No faculties found.")
        except Exception as e:
            raise e

    async def get_faculty_by_id(self, id: int) -> FacultyOut:
        faculty = await self.session.get(Faculty, id)
        try:
            if faculty:
                return FacultyOut(
                    id=faculty.id,
                    name=faculty.name,
                    abbreviation=faculty.abbreviation,
                    buildings=[
                        BuildingOutMinimal(id=building.id, name=building.name)
                        for building in faculty.buildings
                    ],
                )
            raise HTTPException(status_code=404, detail=f"No faculty with id={id}.")
        except Exception as e:
            raise e

    async def add_faculty(self, faculty_data: FacultyIn) -> FacultyOut:
        try:
            new_faculty = Faculty(
                name=faculty_data.name,
                abbreviation=faculty_data.abbreviation,
                buildings=[],
            )
            if faculty_data.buildings:
                result = await self.session.execute(
                    select(Building).where(Building.id.in_(faculty_data.buildings))
                )
                buildings = result.scalars().all()
                if len(buildings) != len(faculty_data.buildings):
                    raise HTTPException(
                        status_code=404,
                        detail=f"One or more buildings not found for IDs {faculty_data.buildings}",
                    )
                for building in buildings:
                    new_faculty.buildings.append(building)
            self.session.add(new_faculty)
            await self.session.commit()
            await self.session.refresh(new_faculty)
            return FacultyOut(
                id=new_faculty.id,
                name=new_faculty.name,
                abbreviation=new_faculty.abbreviation,
                buildings=[
                    BuildingOutMinimal(id=building.id, name=building.name)
                    for building in new_faculty.buildings
                ],
            )
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
                if new_faculty_data.buildings:
                    faculty.buildings = []
                    result = await self.session.execute(
                        select(Building).where(
                            Building.id.in_(new_faculty_data.buildings)
                        )
                    )
                    buildings = result.scalars().all()
                    if len(buildings) != len(new_faculty_data.buildings):
                        raise HTTPException(
                            status_code=404,
                            detail=f"One or more buildings not found for IDs {new_faculty_data.buildings}",
                        )
                    for building in buildings:
                        faculty.buildings.append(building)
                await self.session.commit()
                return FacultyOut(
                    id=faculty.id,
                    name=faculty.name,
                    abbreviation=faculty.abbreviation,
                    buildings=[
                        BuildingOutMinimal(id=building.id, name=building.name)
                        for building in faculty.buildings
                    ],
                )
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
