from fastapi import APIRouter
from .Testpy import router as test_route

router = APIRouter(
    tags=['Test'],
    prefix="/v1"
    )

router.include_router(test_route)