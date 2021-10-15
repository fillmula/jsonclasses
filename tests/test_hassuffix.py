from __future__ import annotations
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestHasSuffix(TestCase):

    def test_hassuffix_validates_a_str_is_suffix_of_original_str(self):
        hs = SuperSuffix(s_hs='this is python')
        hs.validate()

    def test_hassuffix_validates_a_list_is_suffix_of_original_list(self):
        l_hs = SuperSuffix(l_hs=['qq', 'dd', 'ee', 'ff'])
        l_hs.validate()
