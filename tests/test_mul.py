from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestMul(TestCase):


    def test_mul_with_int_value_muls_by_original_value(self):
        mul_int = SimpleCalculation(i_mul=8)
        self.assertEqual(mul_int.i_mul, 40)

    def test_mul_with_float_value_muls_by_original_value(self):
        mul_float = SimpleCalculation(f_mul=7.5)
        self.assertEqual(mul_float.f_mul, 18.75)

    def test_mul_muls_callable_value_to_original_value(self):
        mul_float = SimpleCalculation(c_mul=8.4)
        self.assertEqual(mul_float.c_mul, 21.0)

    def test_mul_muls_types_value_to_original_value(self):
        mul_float = SimpleCalculation(t_mul=8.4)
        self.assertEqual(mul_float.t_mul, 21.0)
