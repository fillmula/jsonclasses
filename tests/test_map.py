from __future__ import annotations
from unittest import TestCase
from tests.classes.super_map import SuperMap


class TestMap(TestCase):

    def test_map_maps_value_by_callable(self):
        item = SuperMap(list1=[0, 1, 2, 3, 4])
        self.assertEqual(item.list1, [1, 2, 3, 4, 5])

    def test_map_maps_value_by_types(self):
        item = SuperMap(list2=[0, 1, 2, 3, 4])
        self.assertEqual(item.list2, [1, 2, 3, 4, 5])
