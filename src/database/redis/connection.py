import datetime
from typing import List

from redis import asyncio as aioredis

from src.config.redis import REDIS_CONFIG
from src.utils.generator import sleep_generator
from src.utils.time import get_now_with_delta


REDIS_CONNECTION = aioredis.from_url(**REDIS_CONFIG.get_redis_attributes(REDIS_CONFIG.api_index))


class RedisSession:
    def __init__(self):
        self.connection = REDIS_CONNECTION

    async def get_keys(self, pattern: str = '*') -> List[str]:
        return [key async for key in sleep_generator(await self.connection.keys(pattern=pattern))]

    async def get_value(self, key: str) -> str | None:
        return await self.connection.get(key)

    async def set_item(
            self,
            key: str,
            value: bytes | str,
            expires: int | datetime.timedelta | datetime.datetime | datetime.date = None
    ):
        await self.connection.set(key, value)
        if isinstance(expires, datetime.timedelta) or isinstance(expires, int):
            await self.connection.expire(key, expires)
        if isinstance(expires, datetime.datetime):
            await self.connection.expire(key, expires - get_now_with_delta())

    async def delete_item(self, key: str):
        await self.connection.delete(key)

    async def delete_values(self, pattern: str = '*'):
        [
            await self.connection.delete(key)
            async for key in sleep_generator(await self.connection.keys(pattern=pattern))
        ]

    async def pop_value(self, key: str) -> str:
        value = await self.get_value(key)
        await self.delete_item(key)
        return value