from __future__ import annotations
from unittest import TestCase
from tests.classes.super_bond import SuperBond


class TestUpperBond(TestCase):

    def test_upper_bond_transforms_int_param_if_it_larger_than_int_val(self):
        n = SuperBond(i_ub=151)
        self.assertEqual(n.i_ub, 150)

    def test_upper_bond_transforms_float_param_if_it_larger_than_float_val(self):
        n = SuperBond(f_ub=151.0)
        self.assertEqual(n.f_ub, 150.0)

    def test_upper_bond_transforms_callable_param_if_it_larger_than_callable_val(self):
        n = SuperBond(c_ub=151)
        self.assertEqual(n.c_ub, 150)

    def test_upper_bond_transforms_types_param_if_it_larger_than_types_val(self):
        n = SuperBond(t_ub=151)
        self.assertEqual(n.t_ub, 150)
