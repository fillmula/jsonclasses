from __future__ import annotations
from unittest import TestCase
from tests.classes.super_bond import SuperBond


class TestLowerBond(TestCase):

    def test_lower_bond_transforms_int_param_if_it_larger_than_int_val(self):
        n = SuperBond(i_lb=149)
        self.assertEqual(n.i_lb, 150)

    def test_lower_bond_transforms_float_param_if_it_larger_than_float_val(self):
        n = SuperBond(f_lb=149.0)
        self.assertEqual(n.f_lb, 150.0)

    def test_lower_bond_transforms_callable_param_if_it_larger_than_callable_val(self):
        n = SuperBond(c_lb=149)
        self.assertEqual(n.c_lb, 150)

    def test_lower_bond_transforms_types_param_if_it_larger_than_types_val(self):
        n = SuperBond(t_lb=149)
        self.assertEqual(n.t_lb, 150)
