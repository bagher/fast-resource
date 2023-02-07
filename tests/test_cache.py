import time
from fast_resource import Resource, cache
import unittest
from fast_resource.cache import RedisCache, MemcachedClient
from redis.client import Redis
from .config import UserResource, inputs
from pymemcache.client.base import Client


class TestResourceCache(unittest.TestCase):
    def setUp(self):
        self.cache = MemcachedClient(Client(server='127.0.0.1:11211'))
        Resource.cache_init(driver=self.cache, prefix='resources.test')
        self.user = UserResource(inputs['bagher'])
        self.users = UserResource.collection(inputs.values())

    def test_resource_constructor(self):
        self.assertIsInstance(self.user, Resource)

    def test_resource_output_cache(self):
        cache(expire_time=1, key="name")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        UserResource.clear_cache_fields()
        self.assertIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def test_resource_output_cache_expire_time(self):
        cache(expire_time=1, key="expire_time")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        UserResource.clear_cache_fields()
        time.sleep(2)
        self.assertNotIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def test_resource_output_cache_with_special_key(self):
        cache(expire_time=1, key="special")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        UserResource.clear_cache_fields()
        self.assertIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def test_resource_cache_delete(self):
        cache(expire_time=1, key="name")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        self.user.cache_delete(['name'])
        UserResource.clear_cache_fields()
        self.assertNotIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def test_resource_cache_delete_rebuild(self):
        cache(expire_time=1, key="cache_delete_rebuild")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        self.user.cache_data = {}
        self.user.cache_delete(['name'], rebuild=True)
        UserResource.clear_cache_fields()
        self.assertIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def test_resource_cache_delete_by_keys(self):
        cache(expire_time=5, key="cache_delete_by_keys")(UserResource.name)
        cache_key = self.user.get_cache_keys('name')
        self.user.to_dict()
        UserResource.cache_delete_by_keys(['cache_delete_by_keys'])
        UserResource.clear_cache_fields()
        self.assertNotIn(
            cache_key,
            self.cache.get([cache_key])
        )

    def tearDown(self):
        Resource.cache_init(driver=None, prefix='')
