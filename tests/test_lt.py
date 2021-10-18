from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestLt(TestCase):

    def test_lt_doesnt_raise_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_lt=5.4)
        n.validate()

    def test_lt_raises_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_lt=5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffLt'],
                         "value is not less than 5.5")

    def test_lt_raises_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_lt=5.6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffLt'],
                         "value is not less than 5.5")

    def test_lt_doesnt_raise_if_int_value_is_less_than_arg(self):
        n = SuperNumber(if_lt=4)
        n.validate()

    def test_lt_raises_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(if_lt=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifLt'],
                         "value is not less than 5")

    def test_lt_raises_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(if_lt=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifLt'],
                         "value is not less than 5")

    def test_lt_doesnt_raise_if_callable_value_is_less_than_arg(self):
        n = SuperNumber(c_lt=4)
        n.validate()

    def test_lt_raises_if_callable_value_is_equal_to_arg(self):
        n = SuperNumber(c_lt=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cLt'],
                         "value is not less than 5")

    def test_lt_raises_if_callable_value_is_greater_than_arg(self):
        n = SuperNumber(c_lt=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cLt'],
                         "value is not less than 5")

    def test_lt_doesnt_raise_if_types_value_is_less_than_arg(self):
        n = SuperNumber(t_lt=4)
        n.validate()

    def test_lt_raises_if_types_value_is_equal_to_arg(self):
        n = SuperNumber(t_lt=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['tLt'],
                         "value is not less than 5")

    def test_lt_raises_if_types_value_is_greater_than_arg(self):
        n = SuperNumber(t_lt=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['tLt'],
                         "value is not less than 5")
