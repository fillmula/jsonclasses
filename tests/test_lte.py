from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestLte(TestCase):

    def test_lte_doesnt_raise_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_lte=5.4)
        n.validate()

    def test_lte_doesnt_raise_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_lte=5.5)
        n.validate()

    def test_lte_raises_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_lte=5.6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffLte'],
                         "value is not less than or equal 5.5")

    def test_lte_doesnt_raise_if_int_value_is_less_than_arg(self):
        n = SuperNumber(if_lte=4)
        n.validate()

    def test_lte_doesnt_raise_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(if_lte=5)
        n.validate()

    def test_lte_raises_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(if_lte=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifLte'],
                         "value is not less than or equal 5")

    def test_lte_doesnt_raise_if_callable_value_is_less_than_arg(self):
        n = SuperNumber(c_lte=4)
        n.validate()

    def test_lte_doesnt_raise_if_callable_value_is_equal_to_arg(self):
        n = SuperNumber(c_lte=5)
        n.validate()

    def test_lte_raises_if_callable_value_is_greater_than_arg(self):
        n = SuperNumber(c_lte=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cLte'],
                         "value is not less than or equal 5")

    def test_lte_doesnt_raise_if_types_value_is_less_than_arg(self):
        n = SuperNumber(t_lte=4)
        n.validate()

    def test_lte_doesnt_raise_if_types_value_is_equal_to_arg(self):
        n = SuperNumber(t_lte=5)
        n.validate()

    def test_lte_raises_if_types_value_is_greater_than_arg(self):
        n = SuperNumber(t_lte=6)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['tLte'],
                         "value is not less than or equal 5")
