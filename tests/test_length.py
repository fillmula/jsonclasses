from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_company import SimpleCompany
from tests.classes.simple_code import SimpleCode


class TestLength(TestCase):

    def test_length_does_not_raise_if_length_is_in_between(self):
        c1 = SimpleCompany(name='AZ', number_of_employees=5)
        c1.validate()
        c2 = SimpleCompany(name='QWERT', number_of_employees=5)
        c2.validate()
        c3 = SimpleCompany(name='QWERTQWERT', number_of_employees=5)
        c3.validate()

    def test_length_raises_if_length_is_lt_lowerbond(self):
        c1 = SimpleCompany(name='Q', number_of_employees=5)
        with self.assertRaises(ValidationException):
            c1.validate()

    def test_length_raises_if_length_is_gt_lowerbond(self):
        c1 = SimpleCompany(name='QWERTYUIOP{', number_of_employees=5)
        with self.assertRaises(ValidationException):
            c1.validate()

    def test_length_should_match_length_in_str(self):
        code = SimpleCode(code='1234')
        code.validate()

    def test_length_should_match_length_in_list(self):
        l_code = SimpleCode(l_code=[1, 2, 3, 4])
        l_code.validate()

    def test_length_raises_if_length_does_not_match_in_str(self):
        code = SimpleCode(code='12345')
        with self.assertRaises(ValidationException):
            code.validate()
        code = SimpleCode(code='1')
        with self.assertRaises(ValidationException):
            code.validate()

    def test_length_raises_if_length_does_not_match_in_list(self):
        l_code = SimpleCode(l_code=[1, 2, 3, 4, 5, 0])
        with self.assertRaises(ValidationException):
            l_code.validate()
        l_code = SimpleCode(l_code=[1, 2])
        with self.assertRaises(ValidationException):
            l_code.validate()

    def test_length_accepts_single_callable_param(self):
        c_code = SimpleCode(c_code='1234')
        c_code.validate()
        c_code = SimpleCode(c_code='12345')
        with self.assertRaises(ValidationException):
            c_code.validate()

    def test_length_accepts_double_callable_param(self):
        cd_code = SimpleCode(cd_code='1234')
        cd_code.validate()
        cd_code = SimpleCode(cd_code='12345')
        cd_code.validate()
        cd_code = SimpleCode(cd_code='123456')
        with self.assertRaises(ValidationException):
            cd_code.validate()
        cd_code = SimpleCode(cd_code='123')
        with self.assertRaises(ValidationException):
            cd_code.validate()

    def test_length_accepts_single_types_param(self):
        t_code = SimpleCode(t_code='1234')
        t_code.validate()
        t_code = SimpleCode(t_code='12345')
        with self.assertRaises(ValidationException):
            t_code.validate()

    def test_length_accepts_double_types_param(self):
        td_code = SimpleCode(td_code='1234')
        td_code.validate()
        td_code = SimpleCode(td_code='12345')
        td_code.validate()
        td_code = SimpleCode(td_code='123456')
        with self.assertRaises(ValidationException):
            td_code.validate()
        td_code = SimpleCode(td_code='123')
        with self.assertRaises(ValidationException):
            td_code.validate()
