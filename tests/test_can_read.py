from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import UnauthorizedActionException
from tests.classes.gs_product import GSProduct, GSProductUser
from tests.classes.gm_product import GMProduct, GMProductUser


class TestCanDelete(TestCase):

    def test_guards_raises_if_no_operator_is_assigned(self):
        product = GSProduct(name='P')
        paid_user = GSProductUser(id='P', name='A', paid_user=True)
        product.user = paid_user
        with self.assertRaises(UnauthorizedActionException):
            product.tojson()

    def test_guard_is_called_for_existing_objects_on_tojson(self):
        product = GSProduct(name='P')
        paid_user = GSProductUser(id='P', name='A', paid_user=True)
        product.user = paid_user
        product.opby(paid_user)
        product.tojson()
        free_user = GSProductUser(id='F', name='A', paid_user=False)
        product.user = free_user
        product.opby(free_user)
        with self.assertRaises(UnauthorizedActionException):
            product.tojson()

    def test_multiple_guards_are_checked_for_existing_objects_on_tojson(self):
        product = GMProduct(name='P')
        setattr(product, '_is_new', False)
        paid_user = GMProductUser(id='P', name='A', paid_user=True)
        product.user = paid_user
        product.opby(paid_user)
        product.tojson()
        free_user = GMProductUser(id='F', name='A', paid_user=False)
        product.user = free_user
        product.opby(free_user)
        with self.assertRaises(UnauthorizedActionException):
            product.tojson()
