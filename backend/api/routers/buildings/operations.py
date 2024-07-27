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
from .utils import building_to_out
from ..faculties.utils import ids_to_faculties
from ..rooms.utils import ids_to_rooms
import logging

logger = logging.getLogger(__name__)


class BuildingsOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_buildings(self, faculty_id: int) -> List[BuildingOut]:
        try:
            if faculty_id:
                logger.info(
                    f"Retrieving all buildings with faculty ID {faculty_id} from database."
                )
                query = (
                    select(Building)
                    .options(joinedload(Building.faculties))
                    .where(Building.faculties_ids.contains([faculty_id]))
                )
            else:
                logger.info("Retrieving all buildings from database.")
                query = select(Building).options(joinedload(Building.faculties))
            result = await self.session.execute(query)
            buildings = result.scalars().unique().all()
            if buildings:
                logger.info("Succesfully retrieved all buildings from database.")
                return [
                    await building_to_out(building)
                    for building in sorted(list(buildings), key=lambda x: x.name)
                ]
            logger.error("No buildings found.")
            raise HTTPException(status_code=404, detail="No buildings found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving buildings:\n{e}"
            )
            raise e

    async def get_building_by_id(self, id: int) -> BuildingOut:
        try:
            logger.info(f"Retrieving building with ID {id} from database.")
            building = await self.session.get(Building, id)
            if building:
                logger.info(
                    f"Succesfully retrieved building with ID {id} from database."
                )
                return await building_to_out(building)
            logger.error(f"No building with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No building with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving building with ID {id}:\n{e}"
            )
            raise e

    async def add_building(self, building_data: BuildingIn) -> BuildingOut:
        try:
            logger.info(f"Adding to database buildind {building_data}")
            new_building = Building(
                name=building_data.name, rooms=[], faculties_ids=[], faculties=[]
            )
            if building_data.faculties:
                new_building.faculties = await ids_to_faculties(
                    self.session, building_data.faculties
                )
                new_building.faculties_ids = building_data.faculties
            if building_data.rooms:
                new_building.rooms = await ids_to_rooms(
                    self.session, building_data.rooms
                )
            self.session.add(new_building)
            await self.session.commit()
            await self.session.refresh(new_building)
            logger.info("Succesfully added new building to database.")
            return await building_to_out(new_building)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding building to databse:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding building to databse:\n{e}"
            )
            raise e

    async def update_building(
        self, id: int, new_building_data: BuildingIn
    ) -> BuildingOut:
        try:
            logger.info(
                f"Updating building with ID {id} with new data: {new_building_data}."
            )
            building = await self.session.get(Building, id)
            if building:
                building.name = new_building_data.name
                if new_building_data.faculties:
                    building.faculties = await ids_to_faculties(
                        self.session, new_building_data.faculties
                    )
                    building.faculties_ids = new_building_data.faculties
                else:
                    building.faculties = []
                    building.faculties_ids = []
                if new_building_data.rooms:
                    building.rooms = await ids_to_rooms(
                        self.session, new_building_data.rooms
                    )
                else:
                    building.rooms = []
                await self.session.commit()
                logger.info(f"Succesfully updated building with ID {id}.")
                return await building_to_out(building)
            logger.error(f"No building with ID {id}")
            raise HTTPException(status_code=404, detail=f"No building with ID {id}.")
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while updating building with ID {id}:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while updating building with ID {id}:\n{e}"
            )
            raise e

    async def delete_building(self, id: int):
        try:
            logger.info(f"Deleting building with ID {id}.")
            building = await self.session.get(Building, id)
            if building:
                await self.session.delete(building)
                await self.session.commit()
                logger.info(f"Succesfully deleted building with ID {id}.")
                return JSONResponse(f"Building with ID {id} deleted.")
            logger.error(f"No building with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No building with ID {id}")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting building with ID {id}:\n{e}"
            )
            raise e
