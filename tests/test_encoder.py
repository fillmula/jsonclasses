from __future__ import annotations
from unittest import TestCase
from jsonclasses import JSONEncoder
from json import dumps
from tests.classes.simple_user import SimpleUser


class TestEncoder(TestCase):

    def test_json_encoder_encodes_str(self):
        user = SimpleUser(name='John', age=5)
        json_str = dumps(user, cls=JSONEncoder)
        self.assertEqual(json_str, '{"name": "John", "age": 5}')

    def test_json_encoder_encodes_list(self):
        user1 = SimpleUser(name='John', age=7)
        user2 = SimpleUser(name='Peter', age=8)
        json_str = dumps([user1, user2], cls=JSONEncoder)
        self.assertEqual(
            json_str,
            '[{"name": "John", "age": 7}, {"name": "Peter", "age": 8}]')
