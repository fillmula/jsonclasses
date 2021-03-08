from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_order import SimpleOrder


class TestIsNew(TestCase):

    def test_jsonclass_object_is_new_on_create(self):
        order = SimpleOrder(quantity=5)
        self.assertEqual(order.is_new, True)

    def test_jsonclass_object_is_new_is_readonly(self):
        order = SimpleOrder(quantity=5)
        with self.assertRaises(AttributeError) as context:
            order.is_new = False
        self.assertEqual(str(context.exception), "can't set attribute")

    def test_jsonclass_object_new_object_wont_record_modified_fields(self):
        order = SimpleOrder(quantity=5)
        order.quantity = 2
        order.quantity = 10
        self.assertEqual(order.modified_fields, ())
