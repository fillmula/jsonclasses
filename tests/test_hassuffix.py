from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_suffix import SuperSuffix
from unittest import TestCase


class TestHasSuffix(TestCase):

    def test_hassuffix_validates_str_param_is_suffix_of_str_val(self):
        s_hs = SuperSuffix(s_hs='this is python')
        s_hs.validate()

    def test_hassuffix_validates_list_param_is_suffix_of_list_val(self):
        l_hs = SuperSuffix(l_hs=['qq', 'dd', 'ee', 'ff'])
        l_hs.validate()

    def test_hassuffix_raises_if_str_param_is_not_suffix_of_str_val(self):
        s_hs = SuperSuffix(s_hs='This ')
        with self.assertRaises(ValidationException) as context:
            s_hs.validate()
        self.assertEqual(context.exception.keypath_messages['sHs'],
                         "suffix is not found")

    def test_hassuffix_raises_if_list_param_is_not_suffix_of_list_val(self):
        l_hs = SuperSuffix(l_hs=['qq'])
        with self.assertRaises(ValidationException) as context:
            l_hs.validate()
        self.assertEqual(context.exception.keypath_messages['lHs'],
                         "suffix is not found")

    def test_hassuffix_validates_callable_param_is_suffix_of_str_val(self):
        c_hs = SuperSuffix(c_hs='this is python')
        c_hs.validate()

    def test_hassuffix_validates_callable_param_is_suffix_of_list_val(self):
        c_l_hs = SuperSuffix(c_l_hs=['qq', 'dd', 'ee', 'ff'])
        c_l_hs.validate()

    def test_hassuffix_raises_if_callable_param_is_not_suffix_of_str_val(self):
        c_hs = SuperSuffix(c_hs='This ')
        with self.assertRaises(ValidationException) as context:
            c_hs.validate()
        self.assertEqual(context.exception.keypath_messages['cHs'],
                         "suffix is not found")

    def test_hassuffix_raises_if_callable_param_is_not_suffix_of_list_val(self):
        c_l_hs = SuperSuffix(c_l_hs=['qq'])
        with self.assertRaises(ValidationException) as context:
            c_l_hs.validate()
        self.assertEqual(context.exception.keypath_messages['cLHs'],
                         "suffix is not found")

    def test_hassuffix_validates_types_param_is_suffix_of_str_val(self):
        t_hs = SuperSuffix(t_hs='this is python')
        t_hs.validate()

    def test_hassuffix_validates_types_param_is_suffix_of_list_val(self):
        t_l_hs = SuperSuffix(t_l_hs=['qq', 'dd', 'ee', 'ff'])
        t_l_hs.validate()

    def test_hassuffix_raises_if_types_param_is_not_suffix_of_str_val(self):
        t_hs = SuperSuffix(t_hs='This ')
        with self.assertRaises(ValidationException) as context:
            t_hs.validate()
        self.assertEqual(context.exception.keypath_messages['tHs'],
                         "suffix is not found")

    def test_hassuffix_raises_if_types_param_is_not_suffix_of_list_val(self):
        t_l_hs = SuperSuffix(t_l_hs=['qq'])
        with self.assertRaises(ValidationException) as context:
            t_l_hs.validate()
        self.assertEqual(context.exception.keypath_messages['tLHs'],
                         "suffix is not found")
