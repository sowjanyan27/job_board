from pydantic_settings import BaseSettings, ConfigDict

class Settings(BaseSettings):
    DEFAULT_PAGE_LIMIT: int = 100
    MAX_PAGE_LIMIT: int = 1000

    # Update Config to use ConfigDict instead
    model_config = ConfigDict(
        env_file=".env"
    )

# Instantiate the settings object
settings = Settings()
