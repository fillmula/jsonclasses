from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_code import SimpleCode

class TestMaxlength(TestCase):

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_constant_maxlength_in_str(self):
        max_code = SimpleCode(max_code='1234')
        max_code.validate()
        max_code = SimpleCode(max_code='12345678')
        max_code.validate()

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_constant_maxlength_in_list(self):
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4])
        l_max_code.validate()
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8])
        l_max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_constant_maxlength_in_str(self):
        max_code = SimpleCode(max_code='1234556932598236')
        with self.assertRaises(ValidationException):
            max_code.validate()
        max_code = SimpleCode(max_code='147432348')
        with self.assertRaises(ValidationException):
            max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_constant_maxlength_in_list(self):
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        with self.assertRaises(ValidationException):
            l_max_code.validate()
        l_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        with self.assertRaises(ValidationException):
            l_max_code.validate()

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_callable_maxlength_in_str(self):
        c_max_code = SimpleCode(c_max_code='1234')
        c_max_code.validate()
        c_max_code = SimpleCode(c_max_code='12345678')
        c_max_code.validate()

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_callable_maxlength_in_list(self):
        cl_max_code = SimpleCode(l_max_code=[1, 2, 3, 4])
        cl_max_code.validate()
        cl_max_code = SimpleCode(l_max_code=[1, 2, 3, 4, 5, 6, 7, 8])
        cl_max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_callable_maxlength_in_str(self):
        c_max_code = SimpleCode(c_max_code='1234556932598236')
        with self.assertRaises(ValidationException):
            c_max_code.validate()
        c_max_code = SimpleCode(c_max_code='147432348')
        with self.assertRaises(ValidationException):
            c_max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_callable_maxlength_in_list(self):
        cl_max_code = SimpleCode(cl_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        with self.assertRaises(ValidationException):
            cl_max_code.validate()
        cl_max_code = SimpleCode(cl_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        with self.assertRaises(ValidationException):
            cl_max_code.validate()

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_types_maxlength_in_str(self):
        t_max_code = SimpleCode(t_max_code='1234')
        t_max_code.validate()
        t_max_code = SimpleCode(t_max_code='12345678')
        t_max_code.validate()

    def test_maxlength_does_not_raise_if_length_is_less_than_or_equal_to_types_maxlength_in_list(self):
        tl_max_code = SimpleCode(tl_max_code=[1, 2, 3, 4])
        tl_max_code.validate()
        tl_max_code = SimpleCode(tl_max_code=[1, 2, 3, 4, 5, 6, 7, 8])
        tl_max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_types_maxlength_in_str(self):
        t_max_code = SimpleCode(t_max_code='1234556932598236')
        with self.assertRaises(ValidationException):
            t_max_code.validate()
        t_max_code = SimpleCode(t_max_code='147432348')
        with self.assertRaises(ValidationException):
            t_max_code.validate()

    def test_maxlength_raises_if_length_is_greater_than_types_maxlength_in_list(self):
        tl_max_code = SimpleCode(tl_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        with self.assertRaises(ValidationException):
            tl_max_code.validate()
        tl_max_code = SimpleCode(tl_max_code=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        with self.assertRaises(ValidationException):
            tl_max_code.validate()
