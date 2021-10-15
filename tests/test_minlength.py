from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_code import SimpleCode

class TestMinlength(TestCase):

    def test_minlength_does_not_raise_if_length_greater_than_or_equal_minlength_in_str(self):
        min_code = SimpleCode(min_code='1234')
        min_code.validate()
        min_code = SimpleCode(min_code='123456')
        min_code.validate()

    def test_minlength_does_not_raise_if_length_greater_than_or_equal_minlength_in_list(self):
        l_min_code = SimpleCode(l_min_code=[1, 2, 3, 4])
        l_min_code.validate()
        l_min_code = SimpleCode(l_min_code=[1, 2, 3, 4, 5])
        l_min_code.validate()

    def test_minlength_raises_if_length_less_than_minlength_in_str(self):
        min_code = SimpleCode(min_code='123')
        with self.assertRaises(ValidationException):
            min_code.validate()
        min_code = SimpleCode(min_code='1')
        with self.assertRaises(ValidationException):
            min_code.validate()

    def test_minlength_raises_if_length_less_than_minlength_in_list(self):
        l_min_code = SimpleCode(l_min_code=[1, 2, 3])
        with self.assertRaises(ValidationException):
            l_min_code.validate()
        l_min_code = SimpleCode(l_min_code=[1])
        with self.assertRaises(ValidationException):
            l_min_code.validate()
