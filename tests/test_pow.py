from __future__ import annotations
from tests.classes.simple_math import SimpleMath
from unittest import TestCase

class TestPow(TestCase):

    def test_pow_with_get_the_value_of_original_value_to_the_power_of_int_value(self):
        p = SimpleMath(i_pow=3)
        self.assertEqual(p.i_pow, 8)

    def test_pow_with_get_the_value_of_original_value_to_the_power_of_float_value(self):
        p = SimpleMath(f_pow=3)
        self.assertEqual(p.f_pow, 15.625)

    def test_pow_with_get_the_value_of_callable_value_to_the_power_of_float_value(self):
        p = SimpleMath(c_pow=3)
        self.assertEqual(p.c_pow, 15.625)

    def test_pow_with_get_the_value_of_types_value_to_the_power_of_float_value(self):
        p = SimpleMath(c_pow=3)
        self.assertEqual(p.c_pow, 15.625)
