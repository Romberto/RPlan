from sys import prefix

from fastapi import APIRouter

router = APIRouter(
    prefix = "/test"
    )

@router.get('/new')
async def testing_router():
    pass