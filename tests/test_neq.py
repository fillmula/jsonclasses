from __future__ import annotations
from tests.classes.simple_eq import SimpleNeq
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestNeq(TestCase):

    def test_neq_does_not_raise_if_is_not_equal(self):
        n = SimpleNeq(neq_value="dsa")
        n.validate()

    def test_neq_raises_if_is_equal(self):
        n = SimpleNeq(neq_value="dsadsa")
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(context.exception.keypath_messages['neqValue'],
                         "value is not unequal")

    def test_neq_does_not_raise_if_unequal_with_callable_value(self):
        e = SimpleNeq(cneq_value="dsa")
        e.validate()

    def test_neq_raises_if_is_equal_with_callable_value(self):
        e = SimpleNeq(cneq_value="dsadsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['cneqValue'],
                         "value is not unequal")

    def test_neq_does_not_raise_if_unequal_with_types_value(self):
        e = SimpleNeq(tneq_value="dsa")
        e.validate()

    def test_neq_raises_if_is_equal_with_types_value(self):
        e = SimpleNeq(tneq_value="dsadsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['tneqValue'],
                         "value is not unequal")
