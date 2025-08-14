from pydantic_settings import BaseSettings
from pydantic import BaseModel

class RunCongig(BaseModel):
    host:str =  "0.0.0.0"
    port: int = 8000

class PrefixApi(BaseModel):
    apiPrefix:str = '/api'




class Settings(BaseSettings):
    run:RunCongig = RunCongig()
    prefix:PrefixApi = PrefixApi()


settings = Settings()