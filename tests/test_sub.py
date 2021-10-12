from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestSub(TestCase):

    def test_sub_calculation_in_int(self):
        sub_int = SimpleCalculation(i_sub=8)
        self.assertEqual(sub_int.i_sub-5, 3)

    def test_sub_calculation_in_float(self):
        sub_float = SimpleCalculation(i_sub=8.5)
        self.assertEqual(sub_float.i_sub-5, 3.5)
