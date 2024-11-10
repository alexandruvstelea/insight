from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date
from ..database.models.vote_limiter import VoteLimiter
from fastapi import HTTPException
from sqlalchemy.future import select
import pytz
import logging

logger = logging.getLogger(__name__)

TIME_SLOTS = [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20), (20, 22)]


def get_utc_now():
    return datetime.now(pytz.utc)


def get_current_time_slot():
    now = datetime.now(pytz.utc).time()
    for start, end in TIME_SLOTS:
        if start <= now.hour < end:
            return f"{start}-{end}"
    return None


async def vote_limiter(client_ip: str, session: AsyncSession):
    try:
        logger.info("Checking if current user can vote.")
        current_slot = get_current_time_slot()
        if not current_slot:
            logger.info("Voting is not allowed at this time.")
            raise HTTPException(
                status_code=403, detail="Voting is not allowed at this time."
            )

        result = await session.execute(
            select(VoteLimiter).where(
                VoteLimiter.ip_address == client_ip,
                VoteLimiter.time_slot == current_slot,
            )
        )
        vote = result.scalar_one_or_none()
        if vote:
            logger.info("User already voted in this time slot.")
            raise HTTPException(
                status_code=403, detail="User already voted in this time slot."
            )

        new_vote = VoteLimiter(
            ip_address=client_ip,
            time_slot=current_slot,
            timestamp=get_utc_now(),
        )
        logger.info(
            f"Added voting record to databse for user with IP {client_ip} at timeslot {current_slot}."
        )
        session.add(new_vote)
        await session.commit()
    except Exception as e:
        logger.error(
            f"An unexpected error has occured while adding voting record:\n{e}"
        )
        raise e
