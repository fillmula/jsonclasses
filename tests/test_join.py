from __future__ import annotations
from tests.classes.super_iterable import SuperIterable
from unittest import TestCase


class TestJoin(TestCase):

    def test_join_keeps_str_value_if_it_is_str(self):
        s = SuperIterable(itsj='asdhakjsh')
        self.assertEqual(s.itsj, 'asdhakjsh')

    def test_join_joins_a_list_of_str_into_a_str(self):
        s = SuperIterable(itsj=["a", "d", "s", "r"])
        self.assertEqual(s.itsj, 'a-d-s-r')

    def test_Join_keeps_callable_value_if_it_is_callable(self):
        s = SuperIterable(c_itsj='asdhakjsh')
        self.assertEqual(s.c_itsj, 'asdhakjsh')

    def test_join_joins_a_types_into_a_types(self):
        s = SuperIterable(t_itsj=["a", "d", "s", "r"])
        self.assertEqual(s.t_itsj, 'a-d-s-r')
