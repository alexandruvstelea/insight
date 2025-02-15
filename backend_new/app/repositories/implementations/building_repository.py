from app.repositories.interfaces.i_building_repository import IBuildingRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from app.models.building import Building
from app.models.faculty import Faculty
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.schemas.building import BuildingFilter
from app.core.logging import logger


class BuildingRepository(IBuildingRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, building: Building) -> Optional[Building]:
        try:
            self.session.add(building)
            await self.session.commit()
            await self.session.refresh(building)
            return building
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(
        self, filters: Optional[BuildingFilter]
    ) -> Optional[list[Building]]:
        try:
            query = select(Building).options(
                joinedload(Building.faculties), joinedload(Building.rooms)
            )

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            return result.scalars().unique().all()
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Building]:
        try:
            query = (
                select(Building)
                .options(
                    joinedload(Building.faculties),
                    joinedload(Building.rooms),
                )
                .where(Building.id == id)
            )

            result = await self.session.execute(query)
            return result.scalars().first()
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, updated_building: Building) -> Optional[Building]:
        try:
            building = await self.get_by_id(id)
            if not building:
                return None

            building.name = updated_building.name
            building.latitude = updated_building.latitude
            building.longitude = updated_building.longitude
            building.faculties = updated_building.faculties
            building.rooms = updated_building.rooms

            await self.session.commit()
            await self.session.refresh(building)
            return building
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            building = await self.get_by_id(id)

            if not building:
                return False

            await self.session.delete(building)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[BuildingFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Building)

            if filters:
                conditions = self._get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def _get_conditions(self, filters: BuildingFilter) -> Optional[list]:
        conditions = []

        if filters.name:
            conditions.append(Building.name == filters.name)
        if filters.faculty_id:
            conditions.append(Building.faculties.any(Faculty.id == filters.faculty_id))

        return conditions if conditions else None
