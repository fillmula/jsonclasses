from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_prefix import SuperPrefix
from unittest import TestCase


class TestIsPrefixOf(TestCase):

    def test_is_prefix_of_validates_str_param_is_prefix_of_str_val(self):
        s_ipo = SuperPrefix(s_ipo='unhappy')
        s_ipo.validate()

    def test_is_prefix_of_validates_list_param_of_int_is_prefix_of_list_val(self):
        loi_ipo = SuperPrefix(loi_ipo=[1, 4, 5, 3, 2, 8])
        loi_ipo.validate()

    def test_is_prefix_of_validates_list_param_of_str_is_prefix_of_list_val(self):
        los_ipo = SuperPrefix(los_ipo=['a', 'd', 'f', 'g'])
        los_ipo.validate()

    def test_is_prefix_of_raises_str_param_is_not_prefix_of_str_val(self):
        s_ipo = SuperPrefix(s_ipo='appy')
        with self.assertRaises(ValidationException) as context:
            s_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['sIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_param_of_int_is_not_prefix_of_list_val(self):
        loi_ipo = SuperPrefix(loi_ipo=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            loi_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['loiIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_param_of_str_is_not_prefix_of_list_val(self):
        los_ipo = SuperPrefix(los_ipo=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            los_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['losIpo'],
                         "prefix is not found")
