from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.responses import JSONResponse

from app.api import api_router
from app.core.config import settings, Settings
from app.core.models.db_helper import DataBaseHelper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await DataBaseHelper.dispose()


my_app = FastAPI(lifespan=lifespan)


@my_app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Database error: {str(exc)}"},
    )


@my_app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Unexpected error: {str(exc)}"},
    )


my_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        "main:my_app", host=settings.run.host, port=settings.run.port, reload=True
    )
