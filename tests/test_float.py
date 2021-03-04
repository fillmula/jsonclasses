from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_balance import SimpleBalance


class TestFloat(TestCase):

    def test_float_is_float_after_assigned(self):
        balance = SimpleBalance(balance=20.2)
        self.assertEqual(balance._data_dict, {'date': None, 'balance': 20.2})

    def test_float_converts_int_into_float(self):
        balance = SimpleBalance(balance=5)
        self.assertEqual(balance.balance, 5.0)
        self.assertEqual(type(balance.balance), float)

    def test_float_raises_if_value_is_not_float(self):
        balance = SimpleBalance(balance='20')
        with self.assertRaises(ValidationException) as context:
            balance.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['balance'],
                         "Value '20' at 'balance' should be float.")

    def test_float_is_float_when_tojson(self):
        balance = SimpleBalance(balance=5.0)
        self.assertEqual(balance.tojson(), {'date': None, 'balance': 5.0})
