from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase


class TestJoin(TestCase):

    def test_Join_keeps_str_value_if_it_is_str(self):
        s = SuperIterable(itsj='asdhakjsh')
        self.assertEqual(s.itsj, 'asdhakjsh')

    def test_join_joins_a_list_of_str_into_a_str(self):
        s = SuperIterable(itsj=["a", "d", "s", "r"])
        self.assertEqual(s.itsj, 'a-d-s-r')
