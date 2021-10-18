from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestIsSuffixOf(TestCase):

    def test_is_suffix_of_validates_str_val_is_suffix_of_str_param(self):
        s_iso = SuperSuffix(s_iso='This is python')
        s_iso.validate()

    def test_is_suffix_of_validates_list_val_is_suffix_of_list_param(self):
        l_iso = SuperSuffix(l_iso=['qq', 'dd', 'ee', 'ff'])
        l_iso.validate()

    def test_is_suffix_of_raises_if_str_val_is_not_suffix_of_str_param(self):
        s_iso = SuperSuffix(s_iso='This ')
        with self.assertRaises(ValidationException) as context:
            s_iso.validate()
        self.assertEqual(context.exception.keypath_messages['sIso'],
                         "suffix is not found")

    def test_is_suffix_of_raises_if_list_val_is_not_suffix_of_list_param(self):
        l_iso = SuperSuffix(l_iso=['qq'])
        with self.assertRaises(ValidationException) as context:
            l_iso.validate()
        self.assertEqual(context.exception.keypath_messages['lIso'],
                         "suffix is not found")
