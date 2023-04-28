from inspect import ismethod
from typing import Dict, List, Tuple
from .resource_cache import ResourceCache


class ResourceCollection:
    def __init__(self, resource, data):
        self.data = data
        self.resource = resource

    def to_dict(self, fields: Tuple = None) -> List[Dict]:
        if self.resource.cache_driver:
            keys = set().union(*(item.get_cache_keys().values() for item in (self.resource(row) for row in self.data)))
            cache_data = self.resource.cache_driver.get(list(keys)) or {}
            output = [
                resource.to_dict(fields=fields, cache_data=cache_data) for resource in
                (self.resource(row) for row in self.data)
            ]
        else:
            output = [self.resource(row).to_dict(fields=fields) for row in self.data]

        return output


class Resource(ResourceCache):

    def __init__(self, input_data: Dict):
        super().__init__()
        self.input_data = input_data

    def __method_exists(self, method: str) -> bool:
        return hasattr(self, method) and ismethod(getattr(self, method))

    def _fetch_data(self, fields: Dict) -> Dict:
        cache_keys = self.get_cache_keys()
        cache_data = self._get_cache_data()
        output_data = {
            field: cache_data[cache_keys[field]] if field in cache_keys and cache_keys[field] in cache_data
            else getattr(self, field)(self.input_data) if self.__method_exists(field)
            else self.input_data[field] if field in self.input_data
            else None
            for field in fields
        }
        return output_data

    def to_dict(self, fields: Tuple = None) -> Dict:
        self._cache_load()
        fields = fields or self.Meta.fields
        output_data = self._fetch_data(fields)
        self._cache_save(output_data)
        return output_data

    @classmethod
    def collection(cls, data: List) -> ResourceCollection:
        return ResourceCollection(cls, data)
