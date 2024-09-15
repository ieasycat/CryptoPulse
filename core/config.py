from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    db_url: str
    echo: bool = True

    class Settings:
        env_file = f"{os.getcwd()}/.env"


settings = Settings()
