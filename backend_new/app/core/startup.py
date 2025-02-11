from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.core.limiter import init_rate_limiter, shutdown_rate_limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_rate_limiter()
    yield
    await shutdown_rate_limiter()
