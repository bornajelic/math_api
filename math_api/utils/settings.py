from datetime import timedelta

from pydantic import BaseSettings, Field


class APIConfig(BaseSettings):
    """
    FastAPI and Redis configuration
    """

    HOST: str = Field(default="redis://host.docker.internal")

    PORT: int = Field(default=6379)

    DB: int = Field(default=0)

    DECODE_RESPONSES: bool = Field(default=True)

    TIMEDELTA: timedelta = Field(default=timedelta(seconds=3600))

    LOG_LEVEL: str = Field(default="INFO")

    JSON_LOGS: int = 0

    FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | PID: {process} | log source: <cyan>{name}</cyan>:<cyan>{function}</cyan> | message: <level>{message}</level>"


api_config = APIConfig()
