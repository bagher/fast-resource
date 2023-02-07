from typing import List, Dict, Union, Callable
from .cache import Cache


def cache(key: Union[Callable, str], expire_time: int = None):
    def decorator(func):
        func.cache = {'key': key, 'expire_time': expire_time}
        return func

    return decorator


class ResourceCache:
    cache_driver = None
    cache_prefix = ""
    cache_fields_config = {}

    def __init__(self):
        self.cache_data = None
        self.cache_fields_alias = {}

    def _cache_load(self):
        if self.cache_driver and self.cache_data is None:
            cache_fields = self.__get_cache_fields_config()
            if cache_fields:
                self.cache_data = self.cache_driver.get(list(self.get_cache_keys().values()))

    @staticmethod
    def clear_cache_fields():
        ResourceCache.cache_fields_config = {}

    def clear_cache_data(self):
        self.cache_data = None

    @classmethod
    def cache_delete_by_keys(cls, keys: List[str]) -> int:
        return cls.cache_driver.delete([f'{cls.cache_prefix}.{key}' for key in keys])

    def __get_cache_fields_config(self) -> Dict:
        class_name = self.__class__
        if class_name not in self.cache_fields_config:
            self.cache_fields_config[class_name] = {}
            for field in self.Meta.fields:
                if hasattr(self, field) and hasattr(getattr(self, field), 'cache'):
                    self.cache_fields_config[class_name][field] = getattr(self, field).cache

        return self.cache_fields_config[class_name]

    def get_cache_keys(self, field_name=None) -> Union[Dict, str]:
        if not self.cache_fields_alias:
            fields = self.__get_cache_fields_config()
            for index, field in fields.items():
                key = field['key'] if isinstance(field['key'], str) else field['key'](self.input_data, index)
                self.cache_fields_alias[index] = f'{self.cache_prefix}.{key}'
        return self.cache_fields_alias[field_name] if field_name else self.cache_fields_alias

    def _get_cache_data(self) -> Dict:
        return self.cache_data or {}

    def _cache_save(self, output_data: Dict) -> None:
        if self.cache_driver:
            for k, value in output_data.items():
                if k in self.get_cache_keys() and self.get_cache_keys(k) not in self.cache_data:
                    self.cache_data[self.get_cache_keys(k)] = value
                    self.cache_driver.set(
                        self.get_cache_keys(k),
                        value,
                        self.__get_cache_fields_config()[k]['expire_time']
                    )

    def cache_delete(self, fields: List = None, rebuild=False) -> int:
        for_remove = []
        fields = fields or self.Meta.fields
        for field in fields:
            if field in self.get_cache_keys():
                for_remove.append(self.get_cache_keys(field))
        total = self.cache_driver.delete(for_remove)
        if rebuild:
            self.cache_data = {}
            output_data = self._fetch_data(fields)
            self._cache_save(output_data)
        return total

    @classmethod
    def cache_init(cls, driver: Cache, prefix="resources"):
        cls.cache_driver = driver
        cls.cache_prefix = prefix
