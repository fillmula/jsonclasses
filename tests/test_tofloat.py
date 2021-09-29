from __future__ import annotations
from unittest import TestCase
from tests.classes.super_type import SuperType


class TestToFloat(TestCase):

    def test_tofloat_transforms_str_into_float(self):
        f = SuperType(tf='-113.0')
        self.assertEqual(f.tf, -113.0)

    def test_tofloat_transforms_bool_into_float(self):
        f = SuperType(tf=False)
        self.assertEqual(f.tf, 0.0)
