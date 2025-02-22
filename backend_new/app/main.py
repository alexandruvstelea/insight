from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.startup import lifespan
from app.core.logging import logger
from app.api.routers.faculty.routers import faculty_router
from app.api.routers.building.routers import building_router
from app.api.routers.professor.routers import professor_router
from app.api.routers.room.routers import room_router
from app.api.routers.programme.routers import programme_router
from app.api.routers.subject.routers import subject_router
from app.api.routers.session.routers import session_router
from app.api.routers.report.routers import report_router

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
app.include_router(professor_router)
app.include_router(room_router)
app.include_router(programme_router)
app.include_router(subject_router)
app.include_router(session_router)
app.include_router(report_router)
