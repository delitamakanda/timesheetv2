import pickle
from typing import Any

import redis.asyncio as aioredis
import ujson
from core.cache.base import BaseBackend
from core.config import config

redis = aioredis.Redis.from_url(config.REDIS_URL)

class RedisBackend(BaseBackend):
    async def get(self, key: str) -> Any:
        result = await redis.get(key)
        if result is None:
            return None
        try:
            return ujson.loads(result.decode('utf-8'))
        except ujson.JSONDecodeError:
            return pickle.loads(result)
        
    async def set(self, value: Any, key: str, expire: int = 60) -> None:
        if isinstance(value, dict):
            value = ujson.dumps(value)
        elif isinstance(value, object):
            value = pickle.dumps(value)
        await redis.set(key, value, expire=expire)
        
    async def delete_startswith(self, value: str) -> None:
        async for key in redis.scan_iter(match=f"{value}*"):
            await redis.delete(key)