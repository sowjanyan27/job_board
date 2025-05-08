# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEFAULT_PAGE_LIMIT: int = 100
    MAX_PAGE_LIMIT: int = 1000

    class Config:
        env_file = ".env"

settings = Settings()
