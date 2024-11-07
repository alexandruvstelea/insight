from ...database.main import get_session
from fastapi import APIRouter, Depends, Header
from .schemas import ReportIn, ReportOut
from sqlalchemy.ext.asyncio import AsyncSession
from .operations import ReportsOperations
from http import HTTPStatus
from fastapi_limiter.depends import RateLimiter
from ...utility.authorizations import authorize
from ..users.utils import get_current_user
from typing import List
import logging

logger = logging.getLogger(__name__)
reports_router = APIRouter(prefix="/api/reports")


@authorize(role=["admin"])
@reports_router.get(
    "/",
    response_model=List[ReportOut],
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_reports(
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> List[ReportOut]:
    logger.info(f"Received GET request on endpoint /api/reports from IP {client_ip}.")
    reports = await ReportsOperations(session).get_reports()
    return reports


@authorize(role=["admin"])
@reports_router.get(
    "/{id}",
    response_model=ReportOut,
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def get_report_by_id(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ReportOut:
    logger.info(
        f"Received GET request on endpoint /api/reports/{id} from IP {client_ip}."
    )
    report = await ReportsOperations(session).get_report_by_id(id)
    return report


@reports_router.post(
    "/",
    response_model=ReportOut,
    dependencies=[Depends(RateLimiter(times=1, minutes=1440))],
    status_code=HTTPStatus.CREATED,
)
async def add_report(
    report_data: ReportIn,
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> ReportOut:
    logger.info(f"Received POST request on endpoint /api/reports from IP {client_ip}.")
    response = await ReportsOperations(session).add_report(report_data)
    return response


@authorize(role=["admin"])
@reports_router.delete(
    "/{id}",
    dependencies=[Depends(RateLimiter(times=50, minutes=1))],
    status_code=HTTPStatus.OK,
)
async def delete_report(
    id: int,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Header(None, alias="X-Real-IP"),
    session: AsyncSession = Depends(get_session),
) -> str:
    logger.info(
        f"Received DELETE request on endpoint /api/reports/{id} from IP {client_ip}."
    )
    response = await ReportsOperations(session).delete_report(id)
    return response
