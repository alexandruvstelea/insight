from app.repositories.interfaces.i_report_repository import IReportRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.exc import IntegrityError
from app.models.report import Report
from app.schemas.report import ReportFilter
from typing import Optional
from app.core.logging import logger


class ReportRepository(IReportRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, report: Report) -> Optional[Report]:
        try:
            self.session.add(report)
            await self.session.commit()
            await self.session.refresh(report)
            return report
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_all(self, filters: Optional[ReportFilter]) -> Optional[list[Report]]:
        try:
            query = select(Report)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            reports = result.scalars().all()

            return reports if reports else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def get_by_id(self, id: int) -> Optional[Report]:
        try:
            report = await self.session.get(Report, id)
            return report if report else None
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def update(self, id: int, new_report: Report) -> Optional[Report]:
        try:
            report = await self.session.get(Report, id)

            if not report:
                return None

            report.timestamp = new_report.timestamp
            report.text = new_report.text

            await self.session.commit()

            return report
        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def delete(self, id: int) -> bool:
        try:
            report = await self.session.get(Report, id)

            if not report:
                return False

            await self.session.delete(report)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    async def count(self, filters: Optional[ReportFilter] = None) -> int:
        try:
            query = select(func.count()).select_from(Report)

            if filters:
                conditions = self.__get_conditions(filters)
                if conditions:
                    query = query.where(and_(*conditions))

            result = await self.session.execute(query)
            count = result.scalar()
            return count if count else 0
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError("Database transaction failed.") from e

    def __get_conditions(filters: ReportFilter) -> Optional[list]:
        conditions = []

        if filters.timestamp_before:
            conditions.append(Report.timestamp <= filters.timestamp_before)
        if filters.timestamp_after:
            conditions.append(Report.timestamp >= filters.timestamp_after)

        return conditions if conditions else None
        # new_report = Report(text=report.text, timestamp=report.timestamp)
