from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_code import SimpleCode

class TestMaxlength(TestCase):

    def test_maxlength_does_not_raise_if_length_less_than_or_equal_maxlength_in_str(self):
        l_max_code = SimpleCode(l_max_code='1234')
        l_max_code.validate()
        l_max_code = SimpleCode(l_max_code='12345678')
        l_max_code.validate()

    def test_maxlength_does_not_raise_if_length_less_than_or_equal_maxlength_in_list(self):
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4])
        l_max_code.validate()
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8])
        l_max_code.validate()

    def test_maxlength_raises_if_length_greater_than_maxlength_in_str(self):
        l_max_code = SimpleCode(l_max_code='12345')
        with self.assertRaises(ValidationException):
            l_max_code.validate()
        l_max_code = SimpleCode(l_max_code='1')
        with self.assertRaises(ValidationException):
            l_max_code.validate()

    def test_maxlength_raises_if_length_greater_than_maxlength_in_str(self):
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        with self.assertRaises(ValidationException):
            l_max_code.validate()
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        with self.assertRaises(ValidationException):
            l_max_code.validate()
