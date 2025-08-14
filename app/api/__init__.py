from fastapi import APIRouter

from app.core.config import settings
from .v1 import router as v1_router

api_router = APIRouter(
    prefix=settings.prefix.apiPrefix
    )
api_router.include_router(v1_router)
