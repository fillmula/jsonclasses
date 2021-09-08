from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.zero_number import ZeroNumber


class TestNonpositive(TestCase):
    def test_nonpositive_doesnt_raise_if_float_value_is_less_than_zero(self):
        n = ZeroNumber(fnonpositive=-5.5)
        n.validate()

    def test_nonpositive_doesnt_raise_if_float_value_is_equal_to_zero(self):
        n = ZeroNumber(fnonpositive=0)
        n.validate()

    def test_nonpositive_raises_if_float_value_is_greater_than_zero(self):
        n = ZeroNumber(fnonpositive=5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fnonpositive'],
                         "value is not nonpositive")

    def test_nonpositive_doesnt_raise_if_int_value_is_less_than_zero(self):
        n = ZeroNumber(inonpositive=-5)
        n.validate()

    def test_nonpositive_doesnt_raise_if_int_value_is_equal_to_zero(self):
        n = ZeroNumber(inonpositive=0)
        n.validate()

    def test_nonpositive_raises_if_int_value_is_greater_than_zero(self):
        n = ZeroNumber(inonpositive=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['inonpositive'],
                         "value is not nonpositive")
