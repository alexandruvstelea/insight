from ...database.models.reports import Report
from .schemas import ReportOut
import logging

logger = logging.getLogger(__name__)


def report_to_out(report: Report) -> ReportOut:
    if report:
        logger.info(f"Converting report with ID {report.id} to ReportOut format.")
        return ReportOut(
            id=report.id,
            text=report.text,
            timestamp=report.timestamp,
        )
    return None
