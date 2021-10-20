from __future__ import annotations
from unittest import TestCase
from tests.classes.super_bond import SuperBond


class TestLowerBond(TestCase):

    def test_lowerbond_transforms_int_param_if_it_is_less_than_int_val(self):
        n = SuperBond(i_lb=-1)
        self.assertEqual(n.i_lb, 1)

    def test_lowerbond_transforms_float_param_if_it_is_less_than_float_val(self):
        n = SuperBond(f_lb=-1.0)
        self.assertEqual(n.f_lb, 1.0)

    def test_lowerbond_transforms_callable_param_if_it_is_less_than_callable_val(self):
        n = SuperBond(c_lb=-1)
        self.assertEqual(n.c_lb, 1)

    def test_lowerbond_transforms_types_param_if_it_is_less_than_types_val(self):
        n = SuperBond(t_lb=-1)
        self.assertEqual(n.t_lb, 1)

    def test_lowerbond_does_not_transform_int_param_if_it_is_greater_than_int_val(self):
        n = SuperBond(i_lb=2)
        self.assertEqual(n.i_lb, 2)

    def test_lowerbond_does_not_transform_float_param_if_it_is_greater_than_float_val(self):
        n = SuperBond(f_lb=2.0)
        self.assertEqual(n.f_lb, 2.0)

    def test_lowerbond_does_not_transform_callable_param_if_it_is_greater_than_callable_val(self):
        n = SuperBond(c_lb=2)
        self.assertEqual(n.c_lb, 2)

    def test_lowerbond_does_not_transform_types_param_if_it_is_greater_than_types_val(self):
        n = SuperBond(t_lb=2)
        self.assertEqual(n.t_lb, 2)
