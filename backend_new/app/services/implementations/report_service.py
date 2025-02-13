from app.services.interfaces.i_report_service import IReportService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report
from app.schemas.report import ReportIn, ReportOut
from typing import Optional
from app.schemas.report import ReportFilter
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils.error_formatter import ErrorFormatter
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ReportService(IReportService):

    def __init__(self, session: AsyncSession):
        super().__init__(session)
