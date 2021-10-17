from __future__ import annotations
from unittest import TestCase
from tests.classes.super_type import SuperType


class TestToStr(TestCase):

    def test_tostr_transforms_int_into_str(self):
        s = SuperType(ts=-122)
        self.assertEqual(s.ts, "-122")

    def test_tostr_transforms_float_into_str(self):
        s = SuperType(ts=-133.99)
        self.assertEqual(s.ts, "-133.99")

    def test_tostr_transforms_bool_into_str(self):
        s = SuperType(ts=False)
        self.assertEqual(s.ts, "False")
