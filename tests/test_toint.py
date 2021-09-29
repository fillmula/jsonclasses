from __future__ import annotations
from unittest import TestCase
from tests.classes.super_type import SuperType


class TestToInt(TestCase):

    def test_toint_transforms_str_into_int(self):
        i = SuperType(ti='-113')
        self.assertEqual(i.ti, -113)

    def test_toint_transforms_bool_into_int(self):
        i = SuperType(ti=False)
        self.assertEqual(i.ti, 0)
