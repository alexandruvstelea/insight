from ...database.models.reports import Report
from .schemas import ReportOut
import logging
import pytz

logger = logging.getLogger(__name__)


def report_to_out(report: Report) -> ReportOut:
    if report:
        logger.info(f"Converting report with ID {report.id} to ReportOut format.")
        ro_timezone = pytz.timezone("Europe/Bucharest")
        if report.timestamp.tzinfo is None:
            report.timestamp = pytz.utc.localize(report.timestamp)
        timestamp_ro = report.timestamp.astimezone(ro_timezone)
        return ReportOut(
            id=report.id,
            text=report.text,
            timestamp=timestamp_ro,
        )
    return None
