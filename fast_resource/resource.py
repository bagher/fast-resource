from inspect import ismethod
from typing import Dict, List, Tuple
from .resource_cache import ResourceCache


class ResourceCollection:
    def __init__(self, resource, data):
        self.data = data
        self.resource = resource

    def to_dict(self, fields: Tuple = None) -> List[Dict]:
        output = []

        if self.resource.cache_driver:
            keys = []
            for row in self.data:
                item = self.resource(row)
                keys += item.get_cache_keys().values()
                output.append(item)
            cache_data = Resource.cache_driver.get(list(set(keys))) or {}
            for index, resource in enumerate(output):
                resource.cache_data = cache_data
                output[index] = resource.to_dict(fields=fields)
                del resource
        else:
            for row in self.data:
                item = self.resource(row)
                output.append(item.to_dict(fields=fields))

        return output


class Resource(ResourceCache):

    def __init__(self, input_data: Dict):
        super().__init__()
        self.input_data = input_data

    def __method_exists(self, method: str) -> bool:
        return hasattr(self, method) and ismethod(getattr(self, method))

    def _fetch_data(self, fields: Dict) -> Dict:
        output_data = {}
        for field in fields:
            if field in self.get_cache_keys() \
                    and self.get_cache_keys(field) in self._get_cache_data():
                output_data[field] = self._get_cache_data()[self.get_cache_keys(field)]
            elif self.__method_exists(field):
                output_data[field] = getattr(self, field)(self.input_data)
            elif field in self.input_data:
                output_data[field] = self.input_data[field]
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
