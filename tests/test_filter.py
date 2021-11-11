from __future__ import annotations
from unittest import TestCase
from tests.classes.super_filter import SuperFilter


class TestFilter(TestCase):

    def test_filter_filters_list_by_callable(self):
        item = SuperFilter(list1=[1, 2, 3, 4])
        self.assertEqual(item.list1, [2, 4])

    def test_filter_filters_list_by_types(self):
        item = SuperFilter(list2=[1, 2, 3, 4])
        self.assertEqual(item.list2, [2, 4])
