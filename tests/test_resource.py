from fast_resource.resource import Resource, ResourceCollection
import unittest
from .config import UserResource, inputs, outputs


class TestResource(unittest.TestCase):
    def setUp(self):
        self.user = UserResource(inputs['bagher'])
        self.users = UserResource.collection(inputs.values())

    def test_resource_constructor(self):
        self.assertIsInstance(self.user, Resource)

    def test_resource_output(self):
        self.assertEqual(self.user.to_dict(), outputs['bagher'])

    def test_resource_output_includes(self):
        self.assertEqual(list(self.user.to_dict(('id',)).keys()), ['id'])

    def test_resource_collection_constructor(self):
        self.assertIsInstance(self.users, ResourceCollection)

    def test_resource_collection_output(self):
        self.assertEqual(self.users.to_dict(), list(outputs.values()))
