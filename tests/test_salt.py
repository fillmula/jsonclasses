from __future__ import annotations
from unittest import TestCase
from tests.classes.super_str import SuperStr
from bcrypt import checkpw


class TestSalt(TestCase):

    def test_salt_add_salt_to_a_string(self):
        ss = SuperStr(password='123456')
        self.assertNotEqual(ss.password, '123456')
        self.assertTrue(checkpw('123456'.encode(), ss.password.encode()))
