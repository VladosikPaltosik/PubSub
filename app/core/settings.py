from functools import lru_cache

from app.core.stream import RedisClient
from pydantic import BaseSettings


VEHICLE_CHANNEL: str = 'pubsub:{}'
VEHICLE_CHANNELS: str = 'pubsub:vehicles'


class Settings(BaseSettings):
    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_DB: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_redis_client():
    settings = Settings()
    return RedisClient(port=settings.REDIS_PORT, host=settings.REDIS_HOST, db=settings.REDIS_DB)
