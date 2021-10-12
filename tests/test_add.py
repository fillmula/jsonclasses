from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestAdd(TestCase):

    def test_add_calculation_in_int(self):
        add_int = SimpleCalculation(i_add=8)
        self.assertEqual(add_int.i_add+5, 13)

    def test_add_calculation_in_float(self):
        add_float = SimpleCalculation(i_add=8.5)
        self.assertEqual(add_float.i_add+5, 13.5)
