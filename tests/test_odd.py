from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_int import SuperInt


class TestOdd(TestCase):

    def test_odd_doesnt_raise_if_int_value_is_odd(self):
        i = SuperInt(i_o=5)
        self.assertEqual(i.i_o, 5)

    def test_odd_raises_if_int_value_is_not_odd(self):
        i = SuperInt(i_o=6)
        with self.assertRaises(ValidationException) as context:
            i.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['iO'],
                         "value is not odd")
