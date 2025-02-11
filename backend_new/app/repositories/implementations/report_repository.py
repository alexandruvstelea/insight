from app.repositories.interfaces.i_report_repository import IReportRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, true
from app.models.report import Report
from app.schemas.report import ReportFilter
from typing import Optional
from app.core.logging import logger


class ReportRepository(IReportRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, report: Report) -> Optional[Report]:
        new_report = Report(text=report.text, timestamp=report.timestamp)

        self.session.add(new_report)
        await self.session.commit()
        await self.session.refresh(new_report)

        return new_report

    async def get_all(self, filters: Optional[ReportFilter]) -> Optional[list[Report]]:
        conditions = []

        if filters.timestamp_before:
            conditions.append(Report.timestamp <= filters.timestamp_before)
        if filters.timestamp_after:
            conditions.append(Report.timestamp >= filters.timestamp_after)

        query = select(Report)
        if conditions:
            query = query.where(and_(*conditions))
        else:
            query = query.where(true())

        result = await self.session.execute(query)
        reports = result.scalars().all()

        return reports if reports else None

    async def get_by_id(self, id: int) -> Optional[Report]:
        report = await self.session.get(Report, id)
        return report if report else None

    async def update(self, id: int, new_report: Report) -> Optional[Report]:
        report = await self.session.get(Report, id)

        if not report:
            return None

        report.timestamp = new_report.timestamp
        report.text = new_report.text

        await self.session.commit()

        return report

    async def delete(self, id: int) -> bool:
        report = await self.session.get(Report, id)

        if not report:
            return False

        await self.session.delete(report)
        await self.session.commit()

        return True
