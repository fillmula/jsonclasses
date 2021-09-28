from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_int import SuperInt


class TestAbs(TestCase):

    def test_abs_keeps_number_value_if_value_is_positive(self):
        i = SuperInt(i_a=5)
        self.assertEqual(i.i_a, 5)

    def test_abs_transforms_nagative_number_value_into_its_absolute_value(self):
        i = SuperInt(i_a=-5)
        self.assertEqual(i.i_a, 5)

