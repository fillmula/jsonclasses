from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase


class TestSplit(TestCase):

    def test_split_keeps_list_value_if_its_list_str(self):
        s = SuperIterable(itssp=["a", "d", "s", "r"])
        self.assertEqual(s.itssp, ["a", "d", "s", "r"])

    def test_split_transforms_if_its_str(self):
        s = SuperIterable(itssp="abc.ous.fga.ssr")
        self.assertEqual(s.itssp, ["abc", "ous", "fga", "ssr"])
