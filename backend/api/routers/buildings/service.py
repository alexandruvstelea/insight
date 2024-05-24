from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.building import Building
from ...database.models.faculty import Faculty
from .schemas import BuildingOut, BuildingIn
from ..faculties.schemas import FacultyOutMinimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error


class BuildingsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_buildings(self) -> List[BuildingOut]:
        try:
            query = select(Building).options(joinedload(Building.faculties))
            result = await self.session.execute(query)
            if result:
                buildings = result.scalars().unique()
                return sorted(list(buildings), key=lambda x: x.name)
            raise HTTPException(status_code=404, detail="No buildings found.")
        except Exception as e:
            raise e

    async def get_building_by_id(self, id: int) -> BuildingOut:
        building = await self.session.get(Building, id)
        try:
            if building:
                return BuildingOut(
                    id=building.id,
                    name=building.name,
                    faculties=[
                        FacultyOutMinimal(
                            id=faculty.id,
                            name=faculty.name,
                            abbreviation=faculty.abbreviation,
                        )
                        for faculty in building.faculties
                    ],
                )
            raise HTTPException(status_code=404, detail=f"No building with id={id}.")
        except Exception as e:
            raise e

    async def add_building(self, building_data: BuildingIn) -> BuildingOut:
        try:
            new_building = Building(name=building_data.name, faculties=[])
            if building_data.faculties:
                result = await self.session.execute(
                    select(Faculty).where(Faculty.id.in_(building_data.faculties))
                )
                faculties = result.scalars().all()
                if len(faculties) != len(building_data.faculties):
                    raise HTTPException(
                        status_code=404,
                        detail=f"One or more faculties not found for IDs {building_data.faculties}",
                    )
                for faculty in faculties:
                    new_building.faculties.append(faculty)
            self.session.add(new_building)
            await self.session.commit()
            await self.session.refresh(new_building)
            return BuildingOut(
                id=new_building.id,
                name=new_building.name,
                faculties=[
                    FacultyOutMinimal(
                        id=faculty.id,
                        name=faculty.name,
                        abbreviation=faculty.abbreviation,
                    )
                    for faculty in new_building.faculties
                ],
            )
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def update_building(
        self, id: int, new_building_data: BuildingIn
    ) -> BuildingOut:
        try:
            building = await self.session.get(Building, id)
            if building:
                building.name = new_building_data.name
                if new_building_data.faculties:
                    building.faculties = []
                    result = await self.session.execute(
                        select(Faculty).where(
                            Faculty.id.in_(new_building_data.faculties)
                        )
                    )
                    faculties = result.scalars().all()
                    if len(faculties) != len(new_building_data.faculties):
                        raise HTTPException(
                            status_code=404,
                            detail=f"One or more faculties not found for IDs {new_building_data.faculties}",
                        )
                    for faculty in faculties:
                        building.faculties.append(faculty)
                await self.session.commit()
                return BuildingOut(
                    id=building.id,
                    name=building.name,
                    faculties=[
                        FacultyOutMinimal(
                            id=faculty.id,
                            name=faculty.name,
                            abbreviation=faculty.abbreviation,
                        )
                        for faculty in building.faculties
                    ],
                )
            raise HTTPException(status_code=404, detail=f"No building with id={id}.")
        except IntegrityError as e:
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            raise e

    async def delete_building(self, id: int):
        try:
            building = await self.session.get(Building, id)
            if building:
                await self.session.delete(building)
                await self.session.commit()
                return JSONResponse(f"Building with ID={id} deleted.")
            else:
                raise HTTPException(status_code=404, detail=f"No building with id={id}")
        except Exception as e:
            raise e
