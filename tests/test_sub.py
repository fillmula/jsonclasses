from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestSub(TestCase):


    def test_sub_with_int_value_sub_original_value(self):
        sub_int = SimpleCalculation(i_sub=8)
        self.assertEqual(sub_int.i_sub, 3)

    def test_sub_with_float_value_sub_original_value(self):
        sub_float = SimpleCalculation(f_sub=8.5)
        self.assertEqual(sub_float.f_sub, 6)
