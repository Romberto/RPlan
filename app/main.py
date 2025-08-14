import uvicorn
from fastapi import FastAPI

from app.api import api_router

my_app = FastAPI()
my_app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run("main:my_app", host="localhost", port=8000, reload=True)
