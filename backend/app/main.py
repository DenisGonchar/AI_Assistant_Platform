from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

from app.core.config import settings
from app.core.logger import logger

from app.database.connection import engine
from app.database.base import Base
import app.database.models  


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    logger.info('Database connection established')
    yield
    logger.info("Application shutdown")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(chat_router)

#-------------------------------------
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
    "message": settings.APP_NAME,
    "version": settings.APP_VERSION,
    'status': 'OK'
    }