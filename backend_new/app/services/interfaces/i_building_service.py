from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.building import Building
from app.repositories.implementations.building_repository import BuildingRepository
from app.schemas.building import BuildingIn, BuildingOut, BuildingFilter
from typing import Optional


class IBuildingService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = BuildingRepository(self.session)

    @abstractmethod
    async def create(self, building: BuildingIn) -> Optional[BuildingOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[BuildingFilter]
    ) -> Optional[list[BuildingOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[BuildingOut]:
        pass

    @abstractmethod
    async def update(self, id: int, building: BuildingIn) -> Optional[BuildingOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[BuildingFilter] = None) -> int:
        pass

    @abstractmethod
    def get_distance(
        self, rating_location: tuple, building: Building
    ) -> Optional[float]:
        pass
