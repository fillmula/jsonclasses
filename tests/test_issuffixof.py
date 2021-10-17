from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestIsSuffixOf(TestCase):

    def test_is_suffix_of_validates_a_str_is_suffix_of_original_str(self):
        s_iso = SuperSuffix(s_iso='This is python')
        s_iso.validate()

    def test_is_suffix_of_validates_a_list_is_suffix_of_original_list(self):
        l_iso = SuperSuffix(l_iso=['qq', 'dd', 'ee', 'ff'])
        l_iso.validate()

    def test_is_suffix_of_raises_if_a_str_is_not_suffix_of_original_str(self):
        s_iso = SuperSuffix(s_iso='This ')
        with self.assertRaises(ValidationException) as context:
            s_iso.validate()
        self.assertEqual(context.exception.keypath_messages['sIso'],
                         "suffix is not found")

    def test_is_suffix_of_raises_if_a_list_is_not_suffix_of_original_list(self):
        l_iso = SuperSuffix(l_iso=['qq'])
        with self.assertRaises(ValidationException) as context:
            l_iso.validate()
        self.assertEqual(context.exception.keypath_messages['lIso'],
                         "suffix is not found")
