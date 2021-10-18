from __future__ import annotations
from tests.classes.simple_eq import SimpleEq
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestEq(TestCase):

    def test_eq_does_not_raise_if_equal(self):
        e = SimpleEq(eq_value="dsadsa")
        e.validate()

    def test_eq_raises_if_is_not_equal(self):
        e = SimpleEq(eq_value="dsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['eqValue'],
                         "value is not equal")

    def test_eq_does_not_raise_if_equal_with_callable_value(self):
        e = SimpleEq(ceq_value="dsadsa")
        e.validate()

    def test_eq_raises_if_is_not_equal_with_callable_value(self):
        e = SimpleEq(ceq_value="dsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['ceqValue'],
                         "value is not equal")

    def test_eq_does_not_raise_if_equal_with_types_value(self):
        e = SimpleEq(teq_value="dsadsa")
        e.validate()

    def test_eq_raises_if_is_not_equal_with_types_value(self):
        e = SimpleEq(teq_value="dsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['teqValue'],
                         "value is not equal")
