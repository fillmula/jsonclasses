from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.zero_number import ZeroNumber


class TestNegative(TestCase):

    def test_negative_doesnt_raise_if_float_value_is_less_than_zero(self):
        n = ZeroNumber(fnegative=-5.5)
        n.validate()

    def test_negative_raises_if_float_value_is_equal_to_zero(self):
        n = ZeroNumber(fnegative=0)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fnegative'],
                         "value is not negative")

    def test_negative_raises_if_float_value_is_greater_than_zero(self):
        n = ZeroNumber(fnegative=5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['fnegative'],
                         "value is not negative")

    def test_negative_doesnt_raise_if_int_value_is_less_than_zero(self):
        n = ZeroNumber(inegative=-5)
        n.validate()

    def test_negative_raises_if_int_value_is_equal_to_zero(self):
        n = ZeroNumber(inegative=0)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['inegative'],
                         "value is not negative")

    def test_negative_raises_if_int_value_is_greater_than_zero(self):
        n = ZeroNumber(inegative=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['inegative'],
                         "value is not negative")
