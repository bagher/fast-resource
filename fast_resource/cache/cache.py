import abc
from typing import Optional, List
import json


class Cache:
    @abc.abstractmethod
    def get(self, key: List) -> Optional[List]:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, key: str, value, expire: Optional[int] = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, keys: List) -> int:
        raise NotImplementedError

    def encode(self, value):
        return json.dumps(value)

    def decode(self, value):
        return json.loads(value)
