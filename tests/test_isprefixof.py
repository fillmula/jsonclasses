from __future__ import annotations
from tests.classes.super_prefix import SuperPrefix
from unittest import TestCase


class TestIsPrefixOf(TestCase):

    def test_is_prefix_of_validates_original_str_is_prefix_of_a_str(self):
        s_ipo = SuperPrefix(s_ipo='unhappy')
        s_ipo.validate()

    def test_is_prefix_of_validates_original_str_is_prefix_of_a_list_of_int(self):
        loi_ipo = SuperPrefix(loi_ipo=[1, 4, 5, 3, 2, 8])
        loi_ipo.validate()

    def test_is_prefix_of_validates_original_str_is_prefix_of_a_list_of_str(self):
        los_ipo = SuperPrefix(los_ipo=['a', 'd', 'f', 'g'])
        los_ipo.validate()
