from sys import prefix

from fastapi import APIRouter

router = APIRouter(prefix="/tests")


@router.get("/new")
async def testing_router():
    return {"message": "success"}
