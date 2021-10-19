from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestIsSuffixOf(TestCase):

    def test_is_suffix_of_validates_str_val_is_suffix_of_str_param(self):
        s_iso = SuperSuffix(s_iso='on')
        s_iso.validate()

    def test_is_suffix_of_validates_list_val_is_suffix_of_list_param(self):
        l_iso = SuperSuffix(l_iso=['ff'])
        l_iso.validate()

    def test_is_suffix_of_raises_if_str_val_is_not_suffix_of_str_param(self):
        s_iso = SuperSuffix(s_iso='py')
        with self.assertRaises(ValidationException) as context:
            s_iso.validate()
        self.assertEqual(context.exception.keypath_messages['sIso'],
                         "suffix is not found")

    def test_is_suffix_of_raises_if_list_val_is_not_suffix_of_list_param(self):
        l_iso = SuperSuffix(l_iso=['ee'])
        with self.assertRaises(ValidationException) as context:
            l_iso.validate()
        self.assertEqual(context.exception.keypath_messages['lIso'],
                         "suffix is not found")

    def test_is_suffix_of_validates_str_val_is_suffix_of_callable_param(self):
        c_iso = SuperSuffix(c_iso='on')
        c_iso.validate()

    def test_is_suffix_of_validates_list_val_is_suffix_of_callable_param(self):
        c_l_iso = SuperSuffix(c_l_iso=['ff'])
        c_l_iso.validate()

    def test_is_suffix_of_raises_if_str_val_is_not_suffix_of_callable_param(self):
        c_iso = SuperSuffix(c_iso='py')
        with self.assertRaises(ValidationException) as context:
            c_iso.validate()
        self.assertEqual(context.exception.keypath_messages['cIso'],
                         "suffix is not found")

    def test_is_suffix_of_raises_if_list_val_is_not_suffix_of_callable_param(self):
        c_l_iso = SuperSuffix(c_l_iso=['ee'])
        with self.assertRaises(ValidationException) as context:
            c_l_iso.validate()
        self.assertEqual(context.exception.keypath_messages['cLIso'],
                         "suffix is not found")

    def test_is_suffix_of_validates_str_val_is_suffix_of_callable_param(self):
        t_iso = SuperSuffix(t_iso='on')
        t_iso.validate()

    def test_is_suffix_of_validates_list_val_is_suffix_of_callable_param(self):
        t_l_iso = SuperSuffix(t_l_iso=['ff'])
        t_l_iso.validate()

    def test_is_suffix_of_raises_if_str_val_is_not_suffix_of_callable_param(self):
        t_iso = SuperSuffix(t_iso='py')
        with self.assertRaises(ValidationException) as context:
            t_iso.validate()
        self.assertEqual(context.exception.keypath_messages['tIso'],
                         "suffix is not found")

    def test_is_suffix_of_raises_if_list_val_is_not_suffix_of_callable_param(self):
        t_l_iso = SuperSuffix(t_l_iso=['ee'])
        with self.assertRaises(ValidationException) as context:
            t_l_iso.validate()
        self.assertEqual(context.exception.keypath_messages['tLIso'],
                         "suffix is not found")
