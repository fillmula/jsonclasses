from __future__ import annotations
from unittest import TestCase
from tests.classes.super_append import SuperAppend

class TestAppend(TestCase):

    def test_append_adds_str_into_the_end_of_original_str(self):
        i_str = SuperAppend(s='99999999')
        self.assertEqual(i_str.s, '999999993432')

    def test_append_adds_int_into_the_end_of_original_list(self):
        l_list = SuperAppend(l=['a', 'c', 's', 'fsa'])
        self.assertEqual(l_list.l, ['a', 'c', 's', 'fsa', '7788'])
