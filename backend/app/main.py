from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.database.connection import engine
from app.database.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    Base.metadata.create_all(bind=engine)
    logger.info('Database initialized')
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

#-------------------------------------
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
    "message": settings.APP_NAME,
    "version": settings.APP_VERSION,
    'status': 'OK'
    }