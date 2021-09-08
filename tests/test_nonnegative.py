from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.zero_number import ZeroNumber


class TestNonnegative(TestCase):
    def test_nonnegative_doesnt_raise_if_float_value_is_greater_than_zero(self):
        n = ZeroNumber(fnonnegative=5.5)
        n.validate()

    def test_nonnegative_doesnt_raise_if_float_value_is_equal_to_zero(self):
        n = ZeroNumber(fnonnegative=0)
        n.validate()

    def test_nonnegative_raises_if_float_value_is_less_than_zero(self):
        n = ZeroNumber(fnonnegative=-5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fnonnegative'],
                         "value is not nonnegative")

    def test_nonnegative_doesnt_raise_if_int_value_is_greater_than_zero(self):
        n = ZeroNumber(inonnegative=5)
        n.validate()

    def test_nonnegative_doesnt_raise_if_int_value_is_equal_to_zero(self):
        n = ZeroNumber(inonnegative=0)
        n.validate()

    def test_nonnegative_raises_if_int_value_is_less_than_zero(self):
        n = ZeroNumber(inonnegative=-5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['inonnegative'],
                         "value is not nonnegative")
