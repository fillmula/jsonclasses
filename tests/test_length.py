from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_company import SimpleCompany
from tests.classes.simple_code import SimpleCode


class TestLength(TestCase):

    def test_length_does_not_raise_length_in_between(self):
        c1 = SimpleCompany(name='AZ', number_of_employees=5)
        c1.validate()
        c2 = SimpleCompany(name='QWERT', number_of_employees=5)
        c2.validate()
        c3 = SimpleCompany(name='QWERTQWERT', number_of_employees=5)
        c3.validate()

    def test_length_raises_length_lt_lower(self):
        c1 = SimpleCompany(name='Q', number_of_employees=5)
        with self.assertRaises(ValidationException):
            c1.validate()

    def test_length_raises_length_gt_lower(self):
        c1 = SimpleCompany(name='QWERTYUIOP{', number_of_employees=5)
        with self.assertRaises(ValidationException):
            c1.validate()

    def test_length_should_be_match(self):
        code = SimpleCode(code='1234')
        code.validate()

    def test_length_raises_if_length_not_match(self):
        code = SimpleCode(code='12345')
        with self.assertRaises(ValidationException):
            code.validate()
        code = SimpleCode(code='1')
        with self.assertRaises(ValidationException):
            code.validate()
