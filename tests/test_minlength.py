from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_code import SimpleCode

class TestMinlength(TestCase):

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_constant_minlength_in_str(self):
        min_code = SimpleCode(min_code='1234')
        min_code.validate()
        min_code = SimpleCode(min_code='123456')
        min_code.validate()

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_constant_minlength_in_list(self):
        l_min_code = SimpleCode(l_min_code=[1, 2, 3, 4])
        l_min_code.validate()
        l_min_code = SimpleCode(l_min_code=[1, 2, 3, 4, 5])
        l_min_code.validate()

    def test_minlength_raises_if_length_is_less_than_constant_minlength_in_str(self):
        min_code = SimpleCode(min_code='123')
        with self.assertRaises(ValidationException):
            min_code.validate()
        min_code = SimpleCode(min_code='1')
        with self.assertRaises(ValidationException):
            min_code.validate()

    def test_minlength_raises_if_length_is_less_than_constant_minlength_in_list(self):
        l_min_code = SimpleCode(l_min_code=[1, 2, 3])
        with self.assertRaises(ValidationException):
            l_min_code.validate()
        l_min_code = SimpleCode(l_min_code=[1])
        with self.assertRaises(ValidationException):
            l_min_code.validate()

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_callable_minlength_in_str(self):
        c_min_code = SimpleCode(c_min_code='1234')
        c_min_code.validate()
        c_min_code = SimpleCode(c_min_code='123456')
        c_min_code.validate()

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_callable_minlength_in_list(self):
        cl_min_code = SimpleCode(cl_min_code=[1, 2, 3, 4])
        cl_min_code.validate()
        cl_min_code = SimpleCode(cl_min_code=[1, 2, 3, 4, 5])
        cl_min_code.validate()

    def test_minlength_raises_if_length_is_less_than_callable_minlength_in_str(self):
        c_min_code = SimpleCode(c_min_code='123')
        with self.assertRaises(ValidationException):
            c_min_code.validate()
        c_min_code = SimpleCode(c_min_code='1')
        with self.assertRaises(ValidationException):
            c_min_code.validate()

    def test_minlength_raises_if_length_is_less_than_callable_minlength_in_list(self):
        cl_min_code = SimpleCode(cl_min_code=[1, 2, 3])
        with self.assertRaises(ValidationException):
            cl_min_code.validate()
        cl_min_code = SimpleCode(cl_min_code=[1])
        with self.assertRaises(ValidationException):
            cl_min_code.validate()

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_types_minlength_in_str(self):
        t_min_code = SimpleCode(t_min_code='1234')
        t_min_code.validate()
        t_min_code = SimpleCode(t_min_code='123456')
        t_min_code.validate()

    def test_minlength_does_not_raise_if_length_is_greater_than_or_equal_to_types_minlength_in_list(self):
        tl_min_code = SimpleCode(tl_min_code=[1, 2, 3, 4])
        tl_min_code.validate()
        tl_min_code = SimpleCode(tl_min_code=[1, 2, 3, 4, 5])
        tl_min_code.validate()

    def test_minlength_raises_if_length_is_less_than_types_minlength_in_str(self):
        t_min_code = SimpleCode(t_min_code='123')
        with self.assertRaises(ValidationException):
            t_min_code.validate()
        t_min_code = SimpleCode(t_min_code='1')
        with self.assertRaises(ValidationException):
            t_min_code.validate()

    def test_minlength_raises_if_length_is_less_than_types_minlength_in_list(self):
        tl_min_code = SimpleCode(tl_min_code=[1, 2, 3])
        with self.assertRaises(ValidationException):
            tl_min_code.validate()
        tl_min_code = SimpleCode(tl_min_code=[1])
        with self.assertRaises(ValidationException):
            tl_min_code.validate()
