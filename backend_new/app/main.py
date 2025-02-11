from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.startup import lifespan
from app.core.logging import logger
from app.api.routers.faculty.routers import faculty_router
from app.api.routers.building.routers import building_router


logger.info("Starting FastAPI REST API for the inSight project.")

app = FastAPI(title="insight-api", lifespan=lifespan, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(faculty_router)
app.include_router(building_router)
