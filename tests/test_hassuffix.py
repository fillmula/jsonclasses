from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestHasSuffix(TestCase):

    def test_hassuffix_validates_str_val_is_suffix_of_str_param(self):
        s_hs = SuperSuffix(s_hs='this is python')
        s_hs.validate()

    def test_hassuffix_validates_list_val_is_suffix_of_list_param(self):
        l_hs = SuperSuffix(l_hs=['qq', 'dd', 'ee', 'ff'])
        l_hs.validate()

    def test_hassuffix_raises_if_str_val_is_not_suffix_of_str_param(self):
        s_hs = SuperSuffix(s_hs='This ')
        with self.assertRaises(ValidationException) as context:
            s_hs.validate()
        self.assertEqual(context.exception.keypath_messages['sHs'],
                         "suffix is not found")

    def test_hassuffix_raises_if_list_val_is_not_suffix_of_list_param(self):
        l_hs = SuperSuffix(l_hs=['qq'])
        with self.assertRaises(ValidationException) as context:
            l_hs.validate()
        self.assertEqual(context.exception.keypath_messages['lHs'],
                         "suffix is not found")
