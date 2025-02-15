from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report
from app.schemas.report import ReportFilter
from typing import Optional


class IReportRepository(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, report: Report) -> Optional[Report]:
        pass

    @abstractmethod
    async def get_all(self, **filters) -> Optional[list[Report]]:
        pass

    @abstractmethod
    async def get_by_id(self) -> Optional[Report]:
        pass

    @abstractmethod
    async def update(self, id: int, report: Report) -> Optional[Report]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    def _get_conditions(self, filters: ReportFilter) -> Optional[list]:
        pass
