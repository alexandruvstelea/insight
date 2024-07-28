from fastapi import FastAPI
from api.routers.faculties.routes import faculties_router
from api.routers.buildings.routes import buildings_router
from api.routers.rooms.routes import rooms_router
from api.routers.programmes.routes import programmes_router
from api.routers.professors.routes import professors_router
from api.routers.subjects.routes import subjects_router
from api.routers.sessions.routes import sessions_router
from api.routers.weeks.routes import weeks_routes
from api.routers.ratings.routes import ratings_routes
from api.routers.comments.routes import comments_routes
from api.routers.users.routes import users_router
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from .database.main import init_db
from .config import settings
import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s\n-> %(message)s\n",
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

logger.info(
    "Starting FastAPI RESTful API for Transylvania University of Brasov feedback system.\n© Alexandru-Vasile Stelea, Andrei Cristian Sava"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    redis_connection = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8"
    )
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()


app = FastAPI(title="feedback-unitbv-api", lifespan=lifespan)


app.include_router(faculties_router)
app.include_router(buildings_router)
app.include_router(rooms_router)
app.include_router(programmes_router)
app.include_router(professors_router)
app.include_router(subjects_router)
app.include_router(sessions_router)
app.include_router(weeks_routes)
app.include_router(ratings_routes)
app.include_router(comments_routes)
app.include_router(users_router)
