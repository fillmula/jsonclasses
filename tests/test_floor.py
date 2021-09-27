from __future__ import annotations
from tests.classes.super_round import SuperRound
from unittest import TestCase



class TestFloor(TestCase):

    def test_floor_transforms_float_value_into_int_by_flooring(self):
        sr = SuperRound(floor_value=19.8)
        self.assertEqual(sr.floor_value, 19)

    def test_floor_keeps_int_value_unchanged(self):
        sr = SuperRound(floor_value=40)
        self.assertEqual(sr.floor_value, 40)




