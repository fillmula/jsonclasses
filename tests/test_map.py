from __future__ import annotations
from unittest import TestCase
from tests.classes.super_map import SuperMap

class TestMap(TestCase):

    def test_map_does_not_raise_if_it_maps_list(self):
        item = SuperMap(l_m=[0, 1, 2, 3, 4])
        self.assertEqual(item.l_m, list(map(lambda a: a +1, [0, 1, 2, 3, 4])))
