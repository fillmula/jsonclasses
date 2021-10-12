from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestMul(TestCase):

    def test_mul_calculation_in_int(self):
        mul_int = SimpleCalculation(i_mul=8)
        self.assertEqual(mul_int.i_mul*5, 40)

    def test_mul_calculation_in_float(self):
        mul_float = SimpleCalculation(i_mul=8.5)
        self.assertEqual(mul_float.i_mul*5, 42.5)
