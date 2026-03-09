from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import router

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router, prefix="/api")
