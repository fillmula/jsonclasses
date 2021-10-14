from __future__ import annotations
from tests.classes.simple_eq import SimpleEq
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestEq(TestCase):

    def test_eq_does_not_raise_if_equal(self):
        e = SimpleEq(eq_value="dsadsa", neq_value="dssa")
        e.validate()

    def test_eq_raises_if_is_not_equal(self):
        e = SimpleEq(eq_value="dsa", neq_value="dsadsa")
        with self.assertRaises(ValidationException) as context:
            e.validate()
        self.assertEqual(context.exception.keypath_messages['eqValue'],
                         "value is not equal")
