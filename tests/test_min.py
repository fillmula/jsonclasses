from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestMin(TestCase):

    def test_min_doesnt_raise_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_min=5.6)
        n.validate()

    def test_min_doesnt_raise_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_min=5.5)
        n.validate()

    def test_min_raises_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_min=5.4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffMin'],
                         "value is not greater than or equal 5.5")

    def test_min_doesnt_raise_if_types_value_is_greater_than_arg(self):
        n = SuperNumber(if_min=6)
        n.validate()

    def test_min_doesnt_raise_if_types_value_is_equal_to_arg(self):
        n = SuperNumber(if_min=5)
        n.validate()

    def test_min_raises_if_types_value_is_less_than_arg(self):
        n = SuperNumber(if_min=4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifMin'],
                         "value is not greater than or equal 5")

    def test_min_doesnt_raise_if_callable_value_is_greater_than_arg(self):
        n = SuperNumber(c_min=6)
        n.validate()

    def test_min_doesnt_raise_if_callable_value_is_equal_to_arg(self):
        n = SuperNumber(c_min=5)
        n.validate()

    def test_min_raises_if_callable_value_is_less_than_arg(self):
        n = SuperNumber(c_min=4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cMin'],
                         "value is not greater than or equal 5")

    def test_min_doesnt_raise_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(t_min=6)
        n.validate()

    def test_min_doesnt_raise_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(t_min=5)
        n.validate()

    def test_min_raises_if_int_value_is_less_than_arg(self):
        n = SuperNumber(t_min=4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['tMin'],
                         "value is not greater than or equal 5")
