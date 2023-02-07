from fastapi import FastAPI
from redis.client import Redis
from fast_resource import Resource, cache
from fast_resource.cache import RedisCache

app = FastAPI()


@app.on_event("startup")
def startup_event():
    Resource.cache_init(driver=RedisCache(Redis()))


@app.get("/")
async def root():
    class UserResource(Resource):
        class Meta:
            fields = (
                'id',
                'name',
            )

        def name(self, input_data):
            return f'{input_data["name"]} {input_data["family"]}'

    return UserResource({'id': '1', 'name': 'bagher', 'family': 'rokni'}).to_dict()
