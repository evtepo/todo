import json
from typing import Any

from redis.asyncio import Redis

from configs.settings import redis_url


class CacheStorage:
    def __init__(self) -> None:
        self.redis = Redis.from_url(redis_url)

    async def get(self, key: str):
        data = await self.redis.get(key)

        if not data:
            return None

        return json.loads(data)

    async def set(self, key: str, value: Any, expire: int):
        await self.redis.set(key, json.dumps(value), expire)


cache = CacheStorage()
