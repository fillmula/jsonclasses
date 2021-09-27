from __future__ import annotations
from tests.classes.super_round import SuperRound
from unittest import TestCase



class TestCeil(TestCase):

    def test_ceil_transforms_float_value_into_int_by_ceiling(self):
        sr = SuperRound(ceil_value=19.8)
        self.assertEqual(sr.ceil_value, 20)

    def test_ceil_keeps_int_value_unchanged(self):
        sr = SuperRound(ceil_value=40)
        self.assertEqual(sr.ceil_value, 40)




