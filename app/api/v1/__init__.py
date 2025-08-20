from fastapi import APIRouter
from .projects import router as project_route

router = APIRouter(prefix="/v1")

router.include_router(project_route)
