from pathlib import Path
import os

from typing import List, ClassVar
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    tags: List[str] = ["CryptoPulse"]


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    env_path: ClassVar[str] = os.getenv(
        "APP_CONFIG_ENV_PATH", str(Path(__file__).parent.parent / ".env")
    )

    model_config = SettingsConfigDict(
        env_file=env_path,
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    binance_api_url: str = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    bringx_api_url: str = "https://open-api.bingx.com/openApi/swap/v2/quote/contracts"


settings = Settings()
