import unittest
from jsonclasses import jsonclass, JSONObject, types
from datetime import datetime, date


class TestReadonlyValidator(unittest.TestCase):

    def test_readonly_fields_will_not_be_set_through_initialization(self):
        @jsonclass(class_graph='test_readonly_1')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.required
        user = User(username='John', role='I want to change haha XD')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': None})

    def test_readonly_fields_will_not_destroy_default_value_through_initialization(self):
        @jsonclass(class_graph='test_readonly_2')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.default('normal').required
        user = User(username='John', role='I want to change haha XD')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': 'normal'})

    def test_readonly_fields_will_be_ok_when_not_provided(self):
        @jsonclass(class_graph='test_readonly_3')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.default('normal').required
        user = User(username='John')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': 'normal'})

    def test_readonly_fields_will_not_be_set_through_set(self):
        @jsonclass(class_graph='test_readonly_4')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.required
        user = User()
        user.set(username='John', role='I want to change haha XD')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': None})

    def test_readonly_fields_will_not_be_erased_through_set(self):
        @jsonclass(class_graph='test_readonly_5')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.default('normal').required
        user = User()
        user.set(username='John', role='I want to change haha XD')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': 'normal'})

    def test_readonly_fields_can_be_modified_directly(self):
        @jsonclass(class_graph='test_readonly_6')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.default('normal').required
        user = User()
        user.set(username='John', role='I want to change haha XD')
        user.role = 'designer'
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': 'designer'})

    def test_readonly_fields_can_be_updated_through_update(self):
        @jsonclass(class_graph='test_readonly_7')
        class User(JSONObject):
            username: str = types.str.required
            role: str = types.str.readonly.default('normal').required
        user = User()
        user.set(username='John', role='I want to change haha XD')
        user.update(role='admin')
        self.assertEqual(user.__fdict__, {'username': 'John', 'role': 'admin'})
