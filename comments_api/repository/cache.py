import json
from abc import ABC, abstractmethod

from redis.asyncio import Redis

from config.settings import settings


class BaseCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, key: str):
        raise NotImplementedError


class RedisRepositroy(BaseCacheStorage):
    def __init__(self, host: str, port: int) -> None:
        self.redis = Redis(host=host, port=port)

    async def get(self, key: str, **kwargs):
        res = await self.redis.get(key)
        if not res:
            return None

        return json.loads(res)

    async def set(self, key: str, value: str, expire: int, **kwargs):
        value = json.dumps(value)
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        keys = await self.redis.keys(key)
        if keys:
            await self.redis.delete(*keys)

    async def close(self):
        await self.redis.close()


cache: BaseCacheStorage | None = RedisRepositroy(host=settings.redis_host, port=settings.redis_port)


async def cache_storage() -> BaseCacheStorage:
    return cache
