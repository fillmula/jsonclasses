from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_len import SimpleLen


class TestLen(TestCase):

    def test_len_returns_length_of_str(self):
        s = SimpleLen()
        self.assertEqual(s.str, 10)

    def test_len_returns_length_of_list(self):
        l = SimpleLen()
        self.assertEqual(l.list, 6)
