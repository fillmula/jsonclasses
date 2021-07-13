from __future__ import annotations
from unittest import TestCase
from tests.classes.cb_product import CBProduct
from tests.classes.cbm_product import CBMProduct
from tests.classes.cbo_product import CBOProduct


class TestDecoratedOnDelete(TestCase):

    def test_callback_are_called_for_existing_objects_on_delete(self):
        p = CBProduct(name='N')
        setattr(p, '_is_new', False)
        p.delete()
        self.assertEqual(p.deleted_count, 99)

    def test_multiple_callbacks_are_called_for_existing_objects_on_del(self):
        p = CBMProduct(name='N')
        setattr(p, '_is_new', False)
        p.delete()
        self.assertEqual(p.deleted_count, 98)

    def test_operator_can_be_passed_into_callback(self):
        p = CBOProduct(name='N')
        setattr(p, '_is_new', False)
        p.opby(10)
        p.delete()
        self.assertEqual(p.deleted_count, 90)
