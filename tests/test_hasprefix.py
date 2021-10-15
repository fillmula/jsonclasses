from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_prefix import SuperPrefix
from unittest import TestCase


class TestHasPrefix(TestCase):

    def test_hasprefix_validates_a_str_is_prefix_of_original_str(self):
        s_hp = SuperPrefix(s_hp='un')
        s_hp.validate()

    def test_hasprefix_validates_a_str_is_prefix_of_original_list_of_int(self):
        loi_hp = SuperPrefix(loi_hp=[1, 4, 5])
        loi_hp.validate()

    def test_hasprefix_validates_a_str_is_prefix_of_original_list_of_str(self):
        los_hp = SuperPrefix(los_hp=['a', 'd'])
        los_hp.validate()
