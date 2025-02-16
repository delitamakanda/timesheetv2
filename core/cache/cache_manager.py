from functools import wraps
from typing import Type
from .base import BaseBackend, BaseKeyMaker
from .cache_tag import CacheTag

class CacheManager:
    def __init__(self):
        self.backends = {}
        self.key_makers = {}
        
    def init(self, backend: Type[BaseBackend], key_maker: Type[BaseKeyMaker]) -> None:
        self.backends = backend
        self.key_makers = key_maker
        
    def cached(self, prefix: str = None, tag: CacheTag = None, ttl: int = 60):
        def _cached(function):
            @wraps(function)
            async def __cached(*args, **kwargs):
                if not self.backends or not self.key_makers:
                    raise ValueError("CacheManager not initialized with backend and key_maker")
                key = await self.key_makers.make(function=function, prefix=prefix if prefix else tag.value)
                cached_response = await self.backends.get(key)
                if cached_response is not None:
                    return cached_response
                response = await function(*args, **kwargs)
                await self.backends.set(response, key, ttl)
                return response
            return __cached
        return _cached
    
    async def remove_by_tag(self, tag: CacheTag) -> None:
        await self.backends.delete_startswith(tag.value)
        
    async  def remove_by_prefix(self, prefix: str) -> None:
        await self.backends.delete_startswith(prefix)
        
Cache = CacheManager()