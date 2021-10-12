from __future__ import annotations
from tests.classes.simple_math import SimpleMath
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestSqrt(TestCase):

    def test_sqrt_with_get_the_square_root_of_int_value(self):
        s = SimpleMath(i_sqrt=4)
        self.assertEqual(s.i_sqrt, 2)

    def test_sqrt_with_get_the_square_root_of_float_value(self):
        s = SimpleMath(f_sqrt=6.25)
        self.assertEqual(s.f_sqrt, 2.5)

    def test_sqrt_raises_if_value_less_or_equal_to_zero(self):
        with self.assertRaises(ValidationException) as context:
            s = SimpleMath(f_sqrt=-6.25)
        self.assertEqual(context.exception.keypath_messages['fSqrt'],
                         "value is less than 0 thus cannot be sqrted")
