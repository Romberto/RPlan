from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn


class RunCongig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class PrefixApi(BaseModel):
    apiPrefix: str = "/api"


class DBConfig(BaseModel):
    url = PostgresDsn
    test_url = PostgresDsn
    echo: bool = (False,)
    echo_pool: bool = (False,)
    max_overflow: int = (10,)
    pool_size: int = (5,)


class Settings(BaseSettings):
    run: RunCongig = RunCongig()
    prefix: PrefixApi = PrefixApi()
    db: DBConfig


settings = Settings()
