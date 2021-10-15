from __future__ import annotations
from unittest import TestCase
from tests.classes.super_wrap import SuperWrap

class TestInterAt(TestCase):

    def test_wrap_into_list_wraps_into_a_list(self):
        s = SuperWrap(s='hfkjd')
        self.assertEqual(s.s, ['hfkjd'])
