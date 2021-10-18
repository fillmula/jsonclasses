from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase


class TestSplit(TestCase):

    def test_split_keeps_list_value_if_it_is_list_of_strs(self):
        s = SuperIterable(itssp=["a", "d", "s", "r"])
        self.assertEqual(s.itssp, ["a", "d", "s", "r"])

    def test_split_splits_str_into_a_list_of_substrs(self):
        s = SuperIterable(itssp="abc.ous.fga.ssr")
        self.assertEqual(s.itssp, ["abc", "ous", "fga", "ssr"])

    def test_split_keeps_callable_value_if_it_is_list_of_strs(self):
        s = SuperIterable(c_itssp=["a", "d", "s", "r"])
        self.assertEqual(s.c_itssp, ["a", "d", "s", "r"])

    def test_split_splits_types_a_list_of_substrs(self):
        s = SuperIterable(t_itssp="abc.ous.fga.ssr")
        self.assertEqual(s.t_itssp, ["abc", "ous", "fga", "ssr"])
