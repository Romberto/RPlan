import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings

my_app = FastAPI()
my_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(
        "main:my_app", host=settings.run.host, port=settings.run.port, reload=True
    )
