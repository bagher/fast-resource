from flask import Flask
from redis.client import Redis
from fast_resource.resource import Resource
from fast_resource import Resource, cache
from fast_resource.cache import RedisCache

app = Flask(__name__)


class UserResource(Resource):
    class Meta:
        fields = (
            'id',
            'name',
        )

    def name(self, input_data):
        return f'{input_data["name"]} {input_data["family"]}'


@app.before_first_request
def before_first_request():
    Resource.cache_init(driver=RedisCache(Redis()))


@app.route("/")
def hello_world():
    return UserResource({'id': '1', 'name': 'bagher', 'family': 'rokni'}).to_dict()
