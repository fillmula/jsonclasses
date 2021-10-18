from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase



class TestReplace(TestCase):

    def test_replace_keeps_str_value_if_no_replacement_is_found(self):
        s = SuperIterable(itsrp="bbbccc")
        self.assertEqual(s.itsrp, "bbbccc")

    def test_replace_replaces_first_appearance(self):
        s = SuperIterable(itsrp="dd qq abc rr")
        self.assertEqual(s.itsrp, "dd qq ABC rr")

    def test_replace_replaces_multiple_appearances(self):
        s = SuperIterable(itsrp="gg ss abc dd abc ee abc")
        self.assertEqual(s.itsrp, "gg ss ABC dd ABC ee ABC")

    def test_replace_replaces_first_appearance_with_callable(self):
        s = SuperIterable(itsrpc="dd qq abc rr")
        self.assertEqual(s.itsrpc, "dd qq ABC rr")
