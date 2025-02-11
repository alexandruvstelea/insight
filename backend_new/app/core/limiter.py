from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from app.core.config import settings


async def init_rate_limiter():
    redis_connection = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8"
    )
    await FastAPILimiter.init(redis_connection)


async def shutdown_rate_limiter():
    await FastAPILimiter.close()
