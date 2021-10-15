from __future__ import annotations
from unittest import TestCase
from tests.classes.super_prepend import SuperPrepend

class TestInterAt(TestCase):

    def test_insert_at_inserts_str_into_original_str(self):
        i_str = SuperPrepend(s='99999999')
        self.assertEqual(i_str.s, '343299999999')

    def test_insert_at_inserts_any_into_original_list(self):
        l_list = SuperPrepend(l=['a', 'c', 's', 'fsa'])
        self.assertEqual(l_list.l, ['7788', 'a', 'c', 's', 'fsa'])
