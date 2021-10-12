from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestDiv(TestCase):

    def test_div_calculation_in_int(self):
        div_int = SimpleCalculation(i_div=8)
        self.assertEqual(div_int.i_div/4, 2)

    def test_div_calculation_in_float(self):
        div_float = SimpleCalculation(i_div=8.5)
        self.assertEqual(div_float.i_div/5, 1.7)
