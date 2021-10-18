from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from classes.super_number import SuperNumber

class TestGt(TestCase):

    def test_gt_doesnt_raise_if_float_value_is_greater_than_arg(self):
        n = SuperNumber(ff_gt=5.6)
        n.validate()

    def test_gt_raises_if_float_value_is_equal_to_arg(self):
        n = SuperNumber(ff_gt=5.5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffGt'],
                         "value is not greater than 5.5")

    def test_gt_raises_if_float_value_is_less_than_arg(self):
        n = SuperNumber(ff_gt=5.4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ffGt'],
                         "value is not greater than 5.5")

    def test_gt_doesnt_raise_if_int_value_is_greater_than_arg(self):
        n = SuperNumber(if_gt=6)
        n.validate()

    def test_gt_raises_if_int_value_is_equal_to_arg(self):
        n = SuperNumber(if_gt=5)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifGt'],
                         "value is not greater than 5")

    def test_gt_raises_if_int_value_is_less_than_arg(self):
        n = SuperNumber(if_gt=4)
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ifGt'],
                         "value is not greater than 5")

    def test_gt_doesnt_raise_if_float_value_is_greater_than_callable_arg(self):
        n = SuperNumber(fcf_gt=5.6)
        n.validate()

    def test_gt_doesnt_raise_if_float_value_is_greater_than_types_arg(self):
        n = SuperNumber(ftf_gt=5.6)
        n.validate()
