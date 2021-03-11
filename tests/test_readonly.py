from __future__ import annotations
from unittest import TestCase
from tests.classes.role_user import RoleUser


class TestReadonlyValidator(TestCase):

    def test_readonly_will_not_be_set_through_init(self):
        user = RoleUser(username='John', role='I want to change haha XD')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'normal'})

    def test_readonly_will_not_override_default_value_through_init(self):
        user = RoleUser(username='John', role='I want to change haha XD')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'normal'})

    def test_readonly_will_be_ok_when_not_provided(self):
        user = RoleUser(username='John')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'normal'})

    def test_readonly_will_not_be_set_through_set(self):
        user = RoleUser()
        user.set(username='John', role='I want to change haha XD')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'normal'})

    def test_readonly_will_not_be_erased_through_set(self):
        user = RoleUser()
        user.set(username='John', role='I want to change haha XD')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'normal'})

    def test_readonly_can_be_modified_directly(self):
        user = RoleUser()
        user.set(username='John', role='I want to change haha XD')
        user.role = 'designer'
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'designer'})

    def test_readonly_can_be_updated_through_update(self):
        user = RoleUser()
        user.set(username='John', role='I want to change haha XD')
        user.update(role='admin')
        self.assertEqual(user._data_dict,
                         {'username': 'John', 'role': 'admin'})
