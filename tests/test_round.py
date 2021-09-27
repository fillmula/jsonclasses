from __future__ import annotations
from tests.classes.super_round import SuperRound
from unittest import TestCase



class TestRound(TestCase):

    def test_round_transforms_value_with_float_point_greater_than_point_5_into_int_by_rounding(self):
        sr = SuperRound(round_value=19.8)
        self.assertEqual(sr.round_value, 20)

    def test_round_transforms_value_with_float_point_less_than_point_5_into_int_by_rounding(self):
        sr = SuperRound(round_value=19.4)
        self.assertEqual(sr.round_value, 19)

    def test_round_keeps_int_value_unchanged(self):
        sr = SuperRound(round_value=40)
        self.assertEqual(sr.round_value, 40)
