from __future__ import annotations
from unittest import TestCase
from tests.classes.password_user import PasswordUser


class TestWriteonly(TestCase):

    def test_writeonly_will_be_ignored_in_output_json_object(self):
        user = PasswordUser(name='John', password='123456')
        self.assertEqual(user.password, '123456')
        json_object = user.tojson()
        self.assertEqual(json_object, {'name': 'John'})
