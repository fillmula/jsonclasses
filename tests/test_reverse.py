from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase



class TestReverse(TestCase):

    def test_reverse_reverses_str(self):
        s = SuperIterable(itsr="Hello Ben")
        self.assertEqual(s.itsr, "neB olleH")

    def test_reverse_reverses_list(self):
        s = SuperIterable(itl=["Hello Ben", 3, True, 6, False])
        self.assertEqual(s.itl, [False, 6, True, 3, "Hello Ben"])
