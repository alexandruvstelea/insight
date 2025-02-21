from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.implementations.report_repository import ReportRepository
from app.schemas.report import ReportIn, ReportOut, ReportFilter
from typing import Optional


class IReportService(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ReportRepository(self.session)

    @abstractmethod
    async def create(self, report_data: ReportIn) -> Optional[ReportOut]:
        pass

    @abstractmethod
    async def get_all(
        self, filters: Optional[ReportFilter]
    ) -> Optional[list[ReportOut]]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[ReportOut]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass

    @abstractmethod
    async def count(self, filters: Optional[ReportFilter]):
        pass
