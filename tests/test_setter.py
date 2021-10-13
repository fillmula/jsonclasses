from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.calc_user import SetterUser


class TestSetter(TestCase):

    def test_setter_sets_correct_value(self):
        user = SetterUser(name="Peter Layber", base_score=25.54)
        user.first_name = 'John'
        self.assertEqual(user.name, 'John Layber')
        user.last_name = 'Nibber'
        self.assertEqual(user.name, 'John Nibber')
        user.score = 100
        self.assertEqual(user.base_score, 50.0)
