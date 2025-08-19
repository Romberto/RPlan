from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunCongig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class PrefixApi(BaseModel):
    apiPrefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn
    test_url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 5
    naming_conventions: dict = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_CONFIG__",
        env_file="app/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    run: RunCongig = RunCongig()
    prefix: PrefixApi = PrefixApi()
    db: DBConfig


settings = Settings()
