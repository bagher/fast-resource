# fast-resource
`fast-resource` is a data transformation layer that sits between the database and the application's users, enabling quick data retrieval. It further enhances performance by caching data using Redis and Memcached.
## Why Use fast-resource?
fast-resource is useful in situations where there are numerous data retrieval queries, multiple data sources requiring data aggregation, and shared data between entities that need to be cached. Additionally, the type of database used is not important.
## Requirements
- `redis`
- `pymemcache`
## Install
```shell
> pip install fast-resource
```
## Usage

### Quick Start

```python
from fast_resource import Resource


class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    def name(self, input_data) -> str:
        return f'{input_data["name"]} {input_data["family"]}'


UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict()
```
### Custom output
```python
UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict(('id',))
```
### Use cache decoder
```python
from redis.client import Redis
from fast_resource import Resource, cache
from fast_resource.cache import RedisCache

def my_key_builder(input_data, field):
    return f'user.{input_data["id"]}.{field}'

class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    @cache(key=my_key_builder)
    def name(self, input_data) -> str:
        return f'{input_data["name"]} {input_data["family"]}'


Resource.cache_init(driver=RedisCache(Redis()))
UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict()
```
### Custom cache expire_time
```python
@cache(key=my_key_builder, expire_time=60)
def name(self, input_data) -> str:
    return f'{input_data["name"]} {input_data["family"]}'
```
### Cache delete
```python
UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).cache_delete()
```
### Cache delete & rebuild
```python
UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).cache_delete(rebuild=True)
```

### Cache delete by keys
```python
UserResource.cache_delete_by_keys(['user.1.name'])
```

### Create collection
```python
user_collection = UserResource.collection([
    {'id': 1, 'name': 'bagher', 'family': 'rokni'},
    {'id': 2, 'name': 'sepehr', 'family': 'rokni'},
    {'id': 3, 'name': 'sama', 'family': 'rokni'},
])
user_collection.to_dict()
```