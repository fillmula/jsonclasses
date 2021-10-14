from __future__ import annotations
from tests.classes.simple_eq import SimpleEq
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestNeq(TestCase):

    def test_neq_does_not_raise_if_is_not_equal(self):
        n = SimpleEq(eq_value="dsadsa", neq_value="dsa")
        n.validate()

    def test_neq_raises_if_is_equal(self):
        n = SimpleEq(eq_value="dsadsa", neq_value="dsadsa")
        with self.assertRaises(ValidationException) as context:
            n.validate()
        self.assertEqual(context.exception.keypath_messages['neqValue'],
                         "value is not unequal")
