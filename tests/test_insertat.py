from __future__ import annotations
from unittest import TestCase
from tests.classes.super_insertat import SuperInsertAt

class TestInterAt(TestCase):

    def test_insert_at_inserts_str_into_original_str(self):
        i_str = SuperInsertAt(s='99999999')
        self.assertEqual(i_str.s, '99943299999')

    def test_insert_at_inserts_any_into_original_list(self):
        l_list = SuperInsertAt(l=['a', 'c', 's', 'fsa'])
        self.assertEqual(l_list.l, ['a', 'E', 'c', 's', 'fsa'])

    def test_insert_at_inserts_callable_str_into_original_str(self):
        i_str = SuperInsertAt(cs='99999999')
        self.assertEqual(i_str.cs, '99943299999')

    def test_insert_at_inserts_types_str_into_original_str(self):
        i_str = SuperInsertAt(ts='99999999')
        self.assertEqual(i_str.ts, '99943299999')
