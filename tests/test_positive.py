from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.zero_number import ZeroNumber


class TestPositive(TestCase):
    def test_positive_doesnt_raise_if_float_value_is_greater_than_zero(self):
        n = ZeroNumber(fpositive=5.5)
        n.validate()

    def test_positive_raises_if_float_value_is_equal_to_zero(self):
        n = ZeroNumber(fpositive=0)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fpositive'],
                         "value is not positive")

    def test_positive_raises_if_float_value_is_less_than_zero(self):
        n = ZeroNumber(fpositive=-5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fpositive'],
                         "value is not positive")

    def test_positive_doesnt_raise_if_int_value_is_greater_than_zero(self):
        n = ZeroNumber(ipositive=5)
        n.validate()

    def test_positive_raises_if_int_value_is_equal_to_zero(self):
        n = ZeroNumber(ipositive=0)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ipositive'],
                         "value is not positive")

    def test_positive_raises_if_int_value_is_less_than_zero(self):
        n = ZeroNumber(ipositive=-5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ipositive'],
                         "value is not positive")
