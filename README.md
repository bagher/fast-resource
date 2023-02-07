# fast-resource
## Introduction
`fast-resource` is a data transformation layer between the database and data returned to the application's users. Also, it can cache data by using Redis and Memcached.
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
from typing import Dict
from fast_resource import Resource


class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    def name(self, input_data: Dict) -> str:
        return f'{input_data["name"]} {input_data["family"]}'


UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict()
```
### Custom output
```python
UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict(('id',))
```
### Use cache decoder
```python
from typing import Dict
from redis.client import Redis
from fast_resource import Resource, cache
from fast_resource.cache import RedisCache

def my_key_builder(input_data, field):
    return f'post.{input_data["id"]}.{field}'


class PostResource(Resource):
    class Meta:
        fields = (
            'id',
            'title',
            'comment_count',
        )

    @cache(key=my_key_builder)
    def comment_count(self, input_data: Dict) -> str:
        return comment.filter(id=input_data['id']).count()


Resource.cache_init(driver=RedisCache(Redis()))
PostResource({'id': 1, 'title': 'Why fast-resource?'}).to_dict()
```
### Custom cache expire_time
```python
    @cache(key=my_key_builder, expire_time=60)
    def comment_count(self, input_data: Dict) -> str:
        return comment.filter(id=input_data['id']).count()
```
### Cache delete
```python
PostResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).cache_delete()
```
### Cache delete & rebuild
```python
PostResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).cache_delete(rebuild=True)
```

### Cache delete by keys
```python
PostResource.cache_delete(['post.1.comment_count'])
```

### Create collection
```python
user_collection = UserResource.collection([
    {'id': 1, 'name': 'bagher', 'family': 'rokni'},
    {'id': 2, 'name': 'sepehr', 'family': 'rokni'}
])
user_collection.to_dict()
```