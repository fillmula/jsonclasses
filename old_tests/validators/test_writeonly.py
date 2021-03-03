import unittest
from jsonclasses import jsonclass, JSONObject, types
from datetime import datetime, date


class TestWriteonlyValidator(unittest.TestCase):

    def test_writeonly_fields_will_be_ignored_in_output_json_object(self):
        @jsonclass(class_graph='test_writeonly_1')
        class User(JSONObject):
            username: str = types.str.required
            password: str = types.str.writeonly.required
        user = User(username='John', password='123456')
        self.assertEqual(user.password, '123456')
        json_object = user.tojson()
        self.assertEqual(json_object, {'username': 'John'})
