from sqlalchemy import select, and_, func
from ...database.models.ratings import Rating
from ...database.models.session import Session
from ...database.models.subject import Subject
from ...database.models.weeks import Week
from ...database.models.room import Room
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from ...utility.error_parsing import format_integrity_error
from .utils import rating_to_out, check_location_distance
from ..sessions.utils import get_session_from_timestamp
from ..subjects.utils import get_session_professor
import logging
from .schemas import (
    RatingOut,
    RatingIn,
    RatingAverageOut,
    WeekRatings,
    GraphDataRatings,
)

logger = logging.getLogger(__name__)


class RatingOperations:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ratings(
        self, professor_id: int, subject_id: int, session_type: str
    ) -> List[RatingOut]:
        try:
            filters = []
            if professor_id:
                filters.append(Rating.professor_id == professor_id)
            if subject_id:
                filters.append(Rating.subject_id == subject_id)
            if session_type:
                filters.append(Rating.session_type == session_type)
            if filters:
                logger.info(f"Retrieving ratings from database with provided filters.")
                query = select(Rating).where(and_(*filters))
            else:
                logger.info(f"Retrieving all ratings from database.")
                query = select(Rating)
            result = await self.session.execute(query)
            ratings = result.scalars().unique().all()
            if ratings:
                logger.info("Succesfully retrieved all ratings from database.")
                return [rating_to_out(rating) for rating in ratings]
            logger.error("No ratings found.")
            raise HTTPException(status_code=404, detail="No ratings found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving ratings:\n{e}"
            )
            raise e

    async def get_ratings_average(
        self, professor_id: int, subject_id: int, session_type: str
    ) -> List[RatingOut]:
        try:
            filters = []
            if professor_id:
                filters.append(Rating.professor_id == professor_id)
            if subject_id:
                filters.append(Rating.subject_id == subject_id)
            if session_type:
                filters.append(Rating.session_type == session_type)
            if filters:
                logger.info(
                    f"Retrieving average ratings from database with provided filters."
                )
                query = select(
                    func.avg(Rating.rating_clarity).label("avg_clarity"),
                    func.avg(Rating.rating_interactivity).label("avg_interactivity"),
                    func.avg(Rating.rating_relevance).label("avg_relevance"),
                    func.avg(Rating.rating_comprehension).label("avg_comprehension"),
                    func.avg(Rating.rating_overall).label("avg_overall"),
                ).where(and_(*filters))
            else:
                logger.info(f"Retrieving all average ratings from database.")
                query = select(
                    func.avg(Rating.rating_clarity).label("avg_clarity"),
                    func.avg(Rating.rating_interactivity).label("avg_interactivity"),
                    func.avg(Rating.rating_relevance).label("avg_relevance"),
                    func.avg(Rating.rating_comprehension).label("avg_comprehension"),
                    func.avg(Rating.rating_overall).label("avg_overall"),
                )
            result = await self.session.execute(query)
            averages = result.fetchone()
            if averages.avg_overall != None:
                logger.info("Succesfully retrieved all average ratings from database.")
                return RatingAverageOut(
                    rating_overall_average=round(averages.avg_overall, 2),
                    rating_clarity_average=round(averages.avg_clarity, 2),
                    rating_interactivity_average=round(averages.avg_interactivity, 2),
                    rating_relevance_average=round(averages.avg_relevance, 2),
                    rating_comprehension_average=round(averages.avg_comprehension, 2),
                )
            logger.error("No ratings found.")
            raise HTTPException(status_code=404, detail="No ratings found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while retrieving average ratings:\n{e}"
            )
            raise e

    async def get_ratings_graph(
        self,
        professor_id: int,
        subject_id: int,
        session_type: str,
    ) -> dict[str, WeekRatings]:
        try:
            filters = []
            if professor_id:
                filters.append(Rating.professor_id == professor_id)
            if subject_id:
                filters.append(Rating.subject_id == subject_id)
            if session_type:
                filters.append(Rating.session_type == session_type)

            if filters:
                logger.info(
                    f"Retrieving graph ratings from database with provided filters."
                )
                query = select(Rating).where(and_(*filters))
            else:
                logger.info(f"Retrieving all graph ratings from database.")
                query = select(Rating)

            result = await self.session.execute(query)
            ratings = result.scalars().unique().all()

            if subject_id:
                query = await self.session.execute(
                    select(Subject.semester).where(Subject.id == subject_id)
                )
                subject_semester = query.scalars().first()
                if subject_semester:
                    query = await self.session.execute(
                        select(Week).where(Week.semester == subject_semester)
                    )
                    weeks = query.scalars().all()
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No subject with ID {subject_id} found.",
                    )
            else:
                query = await self.session.execute(select(Week))
                weeks = query.scalars().all()

            if ratings and weeks:
                graph_data = GraphDataRatings(week_ratings={})
                for week in weeks:
                    week_key = f"week_{week.id}"
                    week_ratings = WeekRatings()
                    clarity_ratings = [
                        rating.rating_clarity
                        for rating in ratings
                        if week.start <= rating.timestamp.date() <= week.end
                    ]
                    interactivity_ratings = [
                        rating.rating_interactivity
                        for rating in ratings
                        if week.start <= rating.timestamp.date() <= week.end
                    ]
                    relevance_ratings = [
                        rating.rating_relevance
                        for rating in ratings
                        if week.start <= rating.timestamp.date() <= week.end
                    ]
                    comprehension_ratings = [
                        rating.rating_comprehension
                        for rating in ratings
                        if week.start <= rating.timestamp.date() <= week.end
                    ]
                    overall_ratings = [
                        rating.rating_overall
                        for rating in ratings
                        if week.start <= rating.timestamp.date() <= week.end
                    ]

                    week_ratings.clarity = (
                        round(sum(clarity_ratings) / len(clarity_ratings), 2)
                        if clarity_ratings
                        else 0
                    )
                    week_ratings.interactivity = (
                        round(
                            sum(interactivity_ratings) / len(interactivity_ratings), 2
                        )
                        if interactivity_ratings
                        else 0
                    )
                    week_ratings.relevance = (
                        round(sum(relevance_ratings) / len(relevance_ratings), 2)
                        if relevance_ratings
                        else 0
                    )
                    week_ratings.comprehension = (
                        round(
                            sum(comprehension_ratings) / len(comprehension_ratings), 2
                        )
                        if comprehension_ratings
                        else 0
                    )
                    week_ratings.overall = (
                        round(sum(overall_ratings) / len(overall_ratings), 2)
                        if overall_ratings
                        else 0
                    )

                    graph_data.week_ratings[week_key] = week_ratings
                logger.info("Retrieved graph ratings.")
                return graph_data.week_ratings
            if not ratings:
                logger.warning("No ratings found.")
                raise HTTPException(status_code=404, detail="No ratings found.")
            if not weeks:
                logger.warning("No weeks found.")
                raise HTTPException(status_code=404, detail="No weeks found.")
        except Exception as e:
            logger.error(
                f"An unexpected error has occurred while retrieving graph ratings:\n{e}"
            )
            raise e

    async def add_rating(self, rating_data: RatingIn) -> RatingOut:
        try:
            logger.info(f"Adding to database rating {rating_data}.")

            if (
                rating_data.rating_clarity < 1
                or rating_data.rating_comprehension < 1
                or rating_data.rating_interactivity < 1
                or rating_data.rating_relevance < 1
            ):
                raise HTTPException(
                    status_code=422,
                    detail=f"Rating data is not valid.",
                )

            query = select(Room).where(Room.unique_code == rating_data.room_code)
            result = await self.session.execute(query)
            room = result.scalars().unique().one_or_none()
            if not room:
                raise HTTPException(
                    status_code=404,
                    detail=f"No room was found with the unique code {rating_data.room_code}.",
                )
            rating_session: Session = await get_session_from_timestamp(
                self.session, rating_data.timestamp, room.id
            )
            if not rating_data.programme_id in [
                programme.id for programme in rating_session.subject.programmes
            ]:
                logger.error(
                    f"Programme ID {rating_data.programme_id} is not valid for current session."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Programme ID {rating_data.programme_id} is not valid for current session.",
                )
            if room.id != rating_session.room_id:
                logger.error(
                    f"Room ID {rating_data.programme_id} is not valid for current session."
                )
                raise HTTPException(
                    status_code=422,
                    detail=f"Room ID {rating_data.programme_id} is not valid for current session.",
                )

            if not check_location_distance(
                (rating_data.latitude, rating_data.longitude),
                (room.building.latitude, room.building.longitude),
            ):
                raise HTTPException(
                    status_code=404,
                    detail=f"No building was found at users location.",
                )

            naive_timestamp = rating_data.timestamp.replace(tzinfo=None)

            new_rating = Rating(
                rating_clarity=rating_data.rating_clarity,
                rating_interactivity=rating_data.rating_interactivity,
                rating_relevance=rating_data.rating_relevance,
                rating_comprehension=rating_data.rating_comprehension,
                rating_overall=(
                    rating_data.rating_clarity
                    + rating_data.rating_interactivity
                    + rating_data.rating_relevance
                    + rating_data.rating_comprehension
                )
                / 4,
                timestamp=naive_timestamp,
                session_type=rating_session.type,
                subject_id=rating_session.subject_id,
                programme_id=rating_data.programme_id,
                room_id=rating_data.room_id,
                professor_id=await get_session_professor(
                    self.session, rating_session.subject_id, rating_session.type
                ),
                faculty_id=rating_session.faculty_id,
            )
            self.session.add(new_rating)
            await self.session.commit()
            await self.session.refresh(new_rating)
            logger.info("Succesfully added new rating to database.")
            return rating_to_out(new_rating)
        except IntegrityError as e:
            error = format_integrity_error(e)
            logger.error(
                f"An integrity error has occured while adding rating to database:\n{e}"
            )
            raise HTTPException(
                status_code=error.get("code"), detail=error.get("detail")
            )
        except Exception as e:
            logger.error(
                f"An unexpected error has occured while adding rating to databse:\n{e}"
            )
            raise e
