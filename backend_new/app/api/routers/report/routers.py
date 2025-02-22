from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.report import ReportIn, ReportOut, ReportFilter
from app.services.implementations.report_service import ReportService
from app.core.database import get_session
from typing import Optional, Literal
from datetime import datetime
from app.core.logging import logger

report_router = APIRouter(prefix="/report", tags=["report"])


@report_router.post("/", response_model=Optional[ReportOut])
async def create(
    subject_data: ReportIn, db_session: AsyncSession = Depends(get_session)
):
    return await ReportService(db_session).create(subject_data)


@report_router.get("/", response_model=Optional[list[ReportOut]])
async def get_all(
    timestamp_after: Optional[datetime] = None,
    timestamp_before: Optional[datetime] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ReportFilter(
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    return await ReportService(db_session).get_all(filters)


@report_router.get("/{report_id}", response_model=Optional[ReportOut])
async def get_by_id(report_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ReportService(db_session).get_by_id(report_id)


@report_router.put("/{report_id}", response_model=Optional[ReportOut])
async def update(
    report_id: int,
    subject_data: ReportIn,
    db_session: AsyncSession = Depends(get_session),
):
    return await ReportService(db_session).update(report_id, subject_data)


@report_router.delete("/{report_id}", response_model=str)
async def delete(report_id: int, db_session: AsyncSession = Depends(get_session)):
    return await ReportService(db_session).delete(report_id)


@report_router.get("/count/entities", response_model=Optional[int])
async def count(
    timestamp_after: Optional[datetime] = None,
    timestamp_before: Optional[datetime] = None,
    db_session: AsyncSession = Depends(get_session),
):
    filters = ReportFilter(
        timestamp_after=timestamp_after,
        timestamp_before=timestamp_before,
    )

    return await ReportService(db_session).count(filters)
