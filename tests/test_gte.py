from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestGte(TestCase):

    def test_gte_doesnt_raise_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_gte=5.6)
        n.validate()

    def test_gte_doesnt_raise_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_gte=5.5)
        n.validate()

    def test_gte_raises_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_gte=5.4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ff_gte'],
                         "value is not greater than or equal 5.5")

    def test_gte_doesnt_raise_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(if_gte=6)
        n.validate()

    def test_gte_doesnt_raise_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(if_gte=5)
        n.validate()

    def test_gte_raises_if_int_value_is_less_than_arg(self):
        n = SuperNumber(if_gte=4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['if_gte'],
                         "value is not greater than or equal 5")
