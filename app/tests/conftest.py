import asyncio

from app.core.settings import get_redis_client
from app.core.stream import RedisClient
from app.main import app
from fakeredis.aioredis import FakeRedis
from httpx import AsyncClient
import pytest


class RedisClientTest(RedisClient):
    def __init__(self) -> None:
        self.client = FakeRedis(decode_responses=True)


def redis_client_test():
    return RedisClientTest()


app.dependency_overrides[get_redis_client] = redis_client_test


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    return AsyncClient(app=app, base_url="http://test")
