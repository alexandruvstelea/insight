from fastapi import FastAPI
from routers import faculties, buildings
from sqlmodel import SQLModel
from databse import engine
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="feedback-iesc-api", lifespan=lifespan)
app.include_router(faculties.router)
app.include_router(buildings.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
