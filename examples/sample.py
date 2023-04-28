from typing import Dict
from redis.client import Redis
from fast_resource import Resource, cache
from fast_resource.cache import RedisCache


def post_cache_key_builder(input_data, field):
    return f'post.{input_data["id"]}.{field}'


class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    def name(self, input_data) -> str:
        return f'{input_data["name"]} {input_data["family"]}'


class PostResource(Resource):
    class Meta:
        fields = (
            'id',
            'title',
            'comment_count',
            'user',
        )

    @cache(key=post_cache_key_builder)
    def comment_count(self, input_data: Dict) -> int:
        return 10

    @cache(key=lambda input_data, field: f'user.{input_data["user_id"]}')
    def user(self, input_data):
        return UserResource({'id': 1, 'name': 'bagher', 'family': 'rokni'}).to_dict()


Resource.cache_init(driver=RedisCache(Redis()))
p = PostResource({'id': 1, 'title': 'Why fast-resource?', 'user_id': 1}).to_dict()
