from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_int import SuperInt


class TestEven(TestCase):

    def test_even_doesnt_raise_if_int_value_is_even(self):
        i = SuperInt(i_e=6)
        self.assertEqual(i.i_e, 6)

    def test_even_raises_if_int_value_is_not_even(self):
        i = SuperInt(i_e=3)
        with self.assertRaises(ValidationException) as context:
            i.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['iE'],
                         "value is not even")
