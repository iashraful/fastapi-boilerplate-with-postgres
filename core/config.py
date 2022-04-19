from typing import List, Union
import os
from pydantic import BaseSettings, validator
from decouple import config


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Boilerplate"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_LEVEL: str = config("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = config("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")

    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = config("SECRET_KEY")
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    CORS_ORIGINS: Union[str, List[str]] = config("CORS_ORIGINS", default=[])

    JWT_SECRET: str = config("JWT_SECRET", default="")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=15)
    REFRESH_TOKEN_EXPIRE_HOURS: int = config("REFRESH_TOKEN_EXPIRE_HOURS", default=2)

    DB_CONN_STRING: str = config("DB_CONN_STRING")
    ASYNC_TESTING_DB_CONN_STRING: str = config(
        "ASYNC_TESTING_DB_CONN_STRING", default=""
    )
    SYNC_TESTING_DB_CONN_STRING: str = config("SYNC_TESTING_DB_CONN_STRING", default="")

    TIMEZONE: str = config("TIMEZONE", default="Asia/Dhaka")

    REDIS_HOST: str = config("REDIS_HOST", default="redis")
    REDIS_PORT: int = config("REDIS_PORT", cast=int, default=6379)
    REDIS_PASS: str = config("REDIS_PASS", default="")
    REDIS_CACHE_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"

    CELERY_BROKER: str = f"redis://{config('REDIS_HOST', default='redis')}:{config('REDIS_PORT', cast=int, default=6379)}/2"
    CELERY_BACKEND: str = f"redis://{config('REDIS_HOST', default='redis')}:{config('REDIS_PORT', cast=int, default=6379)}/2"

    DEFAULT_PAGE_LIMIT: int = 25

    @validator("CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
