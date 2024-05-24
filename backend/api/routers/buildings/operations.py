from sqlalchemy import select
from sqlalchemy.orm import joinedload
from ...database.models.building import Building
from .schemas import BuildingOut, BuildingIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .service import building_to_out, ids_to_faculties


class BuildingsOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_buildings(self) -> List[BuildingOut]:
        try:
            query = select(Building).options(joinedload(Building.faculties))
            result = await self.session.execute(query)
            buildings = result.scalars().unique().all()
            if buildings:
                return sorted(list(buildings), key=lambda x: x.name)
            raise HTTPException(status_code=404, detail="No buildings found.")
        except Exception as e:
            raise e

    async def get_building_by_id(self, id: int) -> BuildingOut:
        building = await self.session.get(Building, id)
        try:
            if building:
                return building_to_out(building)
            raise HTTPException(status_code=404, detail=f"No building with id={id}.")
        except Exception as e:
            raise e

    async def add_building(self, building_data: BuildingIn) -> BuildingOut:
        try:
            new_building = Building(name=building_data.name, faculties=[])
            if building_data.faculties:
                new_building.faculties = await ids_to_faculties(
                    self.session, building_data.faculties
                )
            self.session.add(new_building)
            await self.session.commit()
            await self.session.refresh(new_building)
            return building_to_out(new_building)
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
                    building.faculties = await ids_to_faculties(
                        self.session, new_building_data.faculties
                    )
                else:
                    building.faculties = []
                await self.session.commit()
                return building_to_out(building)
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
