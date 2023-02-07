from .cache import Cache
from typing import List, Dict
from pymemcache.client.base import Client


class MemcachedClient(Cache):
    def __init__(self, memcached: Client):
        self.memcached = memcached

    def get(self, keys: List) -> Dict:
        return {
            index: self.decode(value)
            for index, value in self.memcached.get_many(keys).items()
            if value is not None
        }

    def set(self, key: str, value, expire_time=0) -> None:
        self.memcached.set(key, self.encode(value), expire=expire_time or 0)

    def delete(self, keys: List) -> int:
        return self.memcached.delete_many(keys)
