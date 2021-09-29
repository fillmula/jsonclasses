from __future__ import annotations
from unittest import TestCase
from tests.classes.super_type import SuperType


class TestToList(TestCase):

    def test_tolist_transforms_set_value_into_a_list(self):
        l = SuperType(tl={1, 2, 4, 7, 9})
        self.assertEqual(l.tl, [1, 2, 4, 7, 9])

    def test_tolist_transforms_str_value_into_a_list(self):
        l = SuperType(tl="abc&*(_")
        self.assertEqual(l.tl, ["a", "b", "c", "&", "*", "(", "_"])

    def test_tolist_transforms_tuple_value_into_a_list(self):
        l = SuperType(tl=(1, 2, True, "abc"))
        self.assertEqual(l.tl, [1, 2, True, "abc"])

    def test_tolist_keeps_value_if_type_of_value_is_not_set_str_or_tuple(self):
        l = SuperType(tl=12)
        self.assertEqual(l.tl, 12)

