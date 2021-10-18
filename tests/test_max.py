from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestMax(TestCase):

    def test_max_doesnt_raise_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_max=5.4)
        n.validate()

    def test_max_doesnt_raise_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_max=5.5)
        n.validate()

    def test_max_raises_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_max=5.6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffMax'],
                         "value is not less than or equal 5.5")

    def test_max_doesnt_raise_if_int_value_is_less_than_arg(self):
        n = SuperNumber(if_max=4)
        n.validate()

    def test_max_doesnt_raise_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(if_max=5)
        n.validate()

    def test_max_raises_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(if_max=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifMax'],
                         "value is not less than or equal 5")

    def test_max_doesnt_raise_if_callable_value_is_less_than_arg(self):
        n = SuperNumber(c_max=4)
        n.validate()

    def test_max_doesnt_raise_if_callable_value_is_equal_to_arg(self):
        n = SuperNumber(c_max=5)
        n.validate()

    def test_max_raises_if_callable_value_is_greater_than_arg(self):
        n = SuperNumber(c_max=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cMax'],
                         "value is not less than or equal 5")

    def test_max_doesnt_raise_if_types_value_is_less_than_arg(self):
        n = SuperNumber(t_max=4)
        n.validate()

    def test_max_doesnt_raise_if_types_value_is_equal_to_arg(self):
        n = SuperNumber(t_max=5)
        n.validate()

    def test_max_raises_if_types_value_is_greater_than_arg(self):
        n = SuperNumber(t_max=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['tMax'],
                         "value is not less than or equal 5")
