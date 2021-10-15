from __future__ import annotations
from unittest import TestCase
from tests.classes.super_filter import SuperFilter

class TestFilter(TestCase):

    def test_filter_does_not_raise_if_it_filters_list(self):
        item = SuperFilter(l_fil=[1, 3, 5, 13])
        self.assertEqual(item.l_fil, list(filter(lambda a:a%2, [0, 1, 2, 3, 5, 8, 13])))
