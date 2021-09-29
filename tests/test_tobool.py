from __future__ import annotations
from unittest import TestCase
from tests.classes.super_type import SuperType


class TestToBool(TestCase):

    def test_tobool_transforms_true__if_its_value_is_to_true(self):
        b = SuperType(tb={1, 3, 4})
        self.assertEqual(b.tb, True)

    def test_tobool_transforms_false_if_its_value_is_to_false(self):
        b = SuperType(tb="")
        self.assertEqual(b.tb, False)


