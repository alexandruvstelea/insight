from sqlalchemy import select
from ...database.models.reports import Report
from .schemas import ReportOut, ReportIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import report_to_out
import logging

logger = logging.getLogger(__name__)


class ReportsOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_reports(self) -> List[ReportOut]:
        try:

            logger.info("Retrieving all reports from database.")
            query = select(Report)
            result = await self.session.execute(query)
            reports = result.scalars().unique().all()
            if reports:
                logger.info("Succesfully retrieved all reports from database.")
                return [report_to_out(report) for report in reports]
            logger.error("No reports found.")
            raise HTTPException(status_code=404, detail="No reports found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving reports:\n{e}"
            )
            raise e

    async def get_report_by_id(self, id: int) -> ReportOut:
        try:
            logger.info(f"Retrieving report with ID {id} from database.")
            report = await self.session.get(Report, id)
            if report:
                logger.info(f"Succesfully retrieved report with ID {id} from database.")
                return report_to_out(report)
            logger.error(f"No report with ID {id} found in database.")
            raise HTTPException(status_code=404, detail=f"No report with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving report with ID {id}:\n{e}"
            )
            raise e

    async def add_report(self, report_data: ReportIn) -> ReportOut:
        try:
            logger.info(f"Adding to database report {report_data}.")
            if len(report_data.text) > 500:
                logger.error(
                    f"Report text is too long (lenght {len(report_data.text)}). Maximum text lenght is 500."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Report text is too long (lenght {len(report_data.text)}). Maximum text lenght is 500.",
                )
            if len(report_data.text) < 10:
                logger.error(
                    f"Report text is too short (lenght {len(report_data.text)}). Minimum text lenght is 10."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Report text is too short (lenght {len(report_data.text)}). Minimum text lenght is 10.",
                )

            naive_timestamp = report_data.timestamp.replace(tzinfo=None)
            new_report = Report(text=report_data.text, timestamp=naive_timestamp)

            self.session.add(new_report)
            await self.session.commit()
            await self.session.refresh(new_report)
            logger.info("Succesfully added new report to database.")
            return report_to_out(new_report)
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding report to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding report to databse:\n{e}"
            )
            raise e

    async def delete_report(self, id: int):
        try:
            logger.info(f"Deleting report with ID {id}.")
            report = await self.session.get(Report, id)
            if report:
                await self.session.delete(report)
                await self.session.commit()
                logger.info(f"Succesfully deleted report with ID {id}.")
                return JSONResponse(f"Report with ID={id} deleted.")
            logger.error(f"No report with ID {id}.")
            raise HTTPException(status_code=404, detail=f"No report with ID {id}.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while deleting report with ID {id}:\n{e}"
            )
            raise e
