from __future__ import annotations
from tests.classes.simple_calculation import SimpleCalculation
from unittest import TestCase

class TestAdd(TestCase):

    def test_add_adds_int_value_to_original_value(self):
        add_int = SimpleCalculation(i_add=8)
        self.assertEqual(add_int.i_add, 13)

    def test_add_adds_float_value_to_original_value(self):
        add_float = SimpleCalculation(f_add=8.5)
        self.assertEqual(add_float.f_add, 11)
