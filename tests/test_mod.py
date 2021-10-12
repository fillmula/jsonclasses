from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestMod(TestCase):

    def test_mod_calculation_in_int(self):
        mod_int = SimpleCalculation(i_mod=8)
        self.assertEqual(mod_int.i_mod%5, 3)

    def test_mod_calculation_in_float(self):
        mod_float = SimpleCalculation(i_mod=8.5)
        self.assertEqual(mod_float.i_mod%5, 3.5)
