from sqlalchemy import select, delete, text
from ...database.models.weeks import Week
from .schemas import WeekOut, WeekIn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import week_to_out
from datetime import timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class WeekOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_weeks(self) -> List[WeekOut]:
        try:
            logger.info("Retrieving all weeks from database.")
            query = select(Week)
            result = await self.session.execute(query)
            weeks = result.scalars().unique().all()
            if weeks:
                logger.info("Succesfully retrieved all weeks from database.")
                return [week_to_out(week) for week in weeks]
            logger.error("No weeks found.")
            raise HTTPException(status_code=404, detail="No weeks found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving weeks:\n{e}"
            )
            raise e

    async def add_weeks(self, week_data: WeekIn) -> List[WeekOut]:
        try:
            logger.info(f"Adding to database weeks {week_data}.")
            weeks = []
            counter = 0
            intervals = week_data.intervals
            interval_start = week_data.year_start

            for i in range(0, len(intervals)):
                if i not in [1, 3, 4, 6]:
                    number_of_weeks = intervals[i]
                    for _ in range(number_of_weeks):
                        counter += 1
                        if counter <= 14:
                            semester = 1
                        else:
                            semester = 2
                        end = interval_start + timedelta(days=6)
                        new_week = Week(
                            start=interval_start, end=end, semester=semester
                        )
                        self.session.add(new_week)
                        weeks.append(new_week)
                        interval_start = end + timedelta(days=1)
                else:
                    interval_start += timedelta(days=intervals[i] * 7)
            await self.session.commit()
            for week in weeks:
                await self.session.refresh(week)
            logger.info("Succesfully added new weeks to database.")
            return [week_to_out(week) for week in weeks]
        except IntegrityError as e:
            logger.error(
                f"An integrity error has occured while adding weeks to database:\n{e}"
            )
            error = format_integrity_error(e)
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding weeks to databse:\n{e}"
            )
            raise e

    async def delete_weeks(self):
        try:
            logger.info(f"Deleting weeks from database.")
            reset_sequence_query = text("TRUNCATE TABLE weeks RESTART IDENTITY;")
            await self.session.execute(reset_sequence_query)
            await self.session.commit()
            logger.info(f"Succesfully deleted weeks from database.")
            return JSONResponse("Weeks table has been reset.")
        except SQLAlchemyError as e:
            logger.error(
                f"An unexpected error has occured while deleting weeks from database:\n{e}"
            )
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while resetting the weeks table.\n{e}",
            )
