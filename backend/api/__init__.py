from fastapi import FastAPI
from api.routers.faculties.routes import faculties_router
from api.routers.buildings.routes import buildings_router
from contextlib import asynccontextmanager
from .database.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="feedback-iesc-api", lifespan=lifespan)
app.include_router(faculties_router)
app.include_router(buildings_router)
