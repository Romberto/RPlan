from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings, Settings
from app.core.models.db_helper import DataBaseHelper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await DataBaseHelper.dispose()


my_app = FastAPI(lifespan=lifespan)
my_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        "main:my_app", host=settings.run.host, port=settings.run.port, reload=True
    )
