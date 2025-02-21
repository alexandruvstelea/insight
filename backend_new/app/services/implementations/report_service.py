from app.services.interfaces.i_report_service import IReportService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report
from app.schemas.report import ReportIn, ReportOut
from typing import Optional
from app.schemas.report import ReportFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from pytz import utc
from app.core.logging import logger


class ReportService(IReportService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, report_data: ReportIn) -> Optional[ReportOut]:
        try:
            new_report = Report(text=report_data.text, timestamp=report_data.timestamp)

            if len(new_report.text) > 500 or len(new_report.text) < 10:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Report text must be between 10 and 500 characters.",
                )

            if report_data.timestamp.tzinfo is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Report timestamp has no timezone information.",
                )

            new_report.timestamp = report_data.timestamp.astimezone(utc)

            response = await self.repository.create(new_report)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred while creating new report.",
                )

            return ReportOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    "An unexpected error occurred while creating new report.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while creating new report.",
            )

    async def get_all(
        self, filters: Optional[ReportFilter]
    ) -> Optional[list[ReportOut]]:
        try:
            response = await self.repository.get_all(filters)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No reports found."
                )

            return [ReportOut.model_validate(subject) for subject in response]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while retrieving reports.",
            )

    async def get_by_id(self, id: int) -> Optional[ReportOut]:
        try:
            response = await self.repository.get_by_id(id)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No report found for ID={id}.",
                )

            return ReportOut.model_validate(response)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while retrieving report with ID={id}.",
            )

    async def update(self, id: int, report_data: ReportIn) -> Optional[ReportOut]:
        try:
            new_report = Report(text=report_data.text, timestamp=report_data.timestamp)

            if len(new_report.text) > 500 or len(new_report.text) < 10:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Report text must be between 10 and 500 characters.",
                )

            if report_data.timestamp.tzinfo is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Report timestamp has no timezone information.",
                )

            new_report.timestamp = report_data.timestamp.astimezone(utc)

            response = await self.repository.update(id, new_report)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An unexpected error occurred while updating report with ID={id}.",
                )

            return ReportOut.model_validate(response)
        except IntegrityError as e:
            formatted_error = ErrorFormatter.format_integrity_error(e)
            raise HTTPException(
                status_code=formatted_error.get(
                    "code", status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=formatted_error.get(
                    "detail",
                    f"An unexpected error occurred while updating report with ID={id}.",
                ),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while updating report with ID={id}.{e}",
            )

    async def delete(self, id: int) -> bool:
        try:
            response = await self.repository.delete(id)
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No report with ID={id} found.",
                )
            return JSONResponse(f"Report with ID {id} deleted.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred while deleting report with ID={id}.",
            )

    async def count(self, filters: Optional[ReportFilter]):
        try:
            count = await self.repository.count(filters)
            return count
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while counting reports.",
            )
