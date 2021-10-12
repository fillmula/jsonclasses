from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestDiv(TestCase):


    def test_div_with_int_value_divs_by_original_value_(self):
        div_int = SimpleCalculation(i_div=10)
        self.assertEqual(div_int.i_div, 2)

    def test_div_with_float_value_divs_by_original_value_(self):
        div_float = SimpleCalculation(f_div=7.5)
        self.assertEqual(div_float.f_div, 3)
