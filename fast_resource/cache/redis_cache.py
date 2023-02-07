from .cache import Cache
from typing import List, Dict
from redis.client import Redis


class RedisCache(Cache):
    def __init__(self, redis: Redis):
        self.redis = redis

    def get(self, keys: List) -> Dict:
        return {
            keys[index]: self.decode(value) for index, value in enumerate(self.redis.mget(keys))
            if value is not None
        }

    def set(self, key, value, expire_time=None) -> None:
        self.redis.set(key, self.encode(value), ex=expire_time)

    def delete(self, keys: List) -> int:
        return self.redis.delete(*keys)
