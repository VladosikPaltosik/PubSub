from typing import Union

import orjson
from redis.asyncio import Redis


class RedisClient:
    def __init__(self, port: int, host: str, db: str | int):
        self.client = Redis(port=port, host=host, db=db)

    async def publish(self, channel: str, data: Union[dict, list]) -> None:
        await self.client.publish(channel=channel, message=orjson.dumps(data))

    async def set_item(self, name: str, value: str) -> None:
        await self.client.set(name=name, value=value, ex=60)

    async def get_items(self) -> list:
        items = await self.client.keys()
        return [item.decode('utf-8') for item in items]
