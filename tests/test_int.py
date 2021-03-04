from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_order import SimpleOrder


class TestInt(TestCase):

    def test_int_is_int_after_assigned(self):
        order = SimpleOrder(quantity=5)
        self.assertEqual(order._data_dict, {'name': None, 'quantity': 5})

    def test_int_raises_if_value_is_not_int(self):
        order = SimpleOrder(quantity=10.5)
        with self.assertRaises(ValidationException) as context:
            order.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['quantity'],
                         "Value '10.5' at 'quantity' should be int.")

    def test_int_is_int_when_tojson(self):
        order = SimpleOrder(quantity=5)
        self.assertEqual(order.tojson(), {'name': None, 'quantity': 5})
