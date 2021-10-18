from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase


class TestReplacer(TestCase):

    def test_replacer_keeps_str_value_if_no_replacement_is_found(self):
        s = SuperIterable(itssub="bbbccc")
        self.assertEqual(s.itssub, "bbbccc")

    def test_replacer_replaces_first_appearance(self):
        s = SuperIterable(itssub="dd qq 1 rr")
        self.assertEqual(s.itssub, "dd qq ABC rr")

    def test_replacer_replaces_multiple_appearances(self):
        s = SuperIterable(itssub="gg ss 2 dd 5 ee 8")
        self.assertEqual(s.itssub, "gg ss ABC dd ABC ee ABC")

    def test_replacer_keeps_callable_value_if_no_replacement_is_found(self):
        s = SuperIterable(c_itssub="bbbccc")
        self.assertEqual(s.c_itssub, "bbbccc")

    def test_replacer_keeps_types_value_if_no_replacement_is_found(self):
        s = SuperIterable(t_itssub="bbbccc")
        self.assertEqual(s.t_itssub, "bbbccc")
