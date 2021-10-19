from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_prefix import IsPrefixOf
from unittest import TestCase


class TestIsPrefixOf(TestCase):

    def test_is_prefix_of_validates_str_val_is_prefix_of_str_param(self):
        s_ipo = IsPrefixOf(s_ipo='unha')
        s_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_int_is_prefix_of_list_param(self):
        loi_ipo = IsPrefixOf(loi_ipo=[1, 4, 5])
        loi_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_str_is_prefix_of_list_param(self):
        los_ipo = IsPrefixOf(los_ipo=['a', 'd'])
        los_ipo.validate()

    def test_is_prefix_of_raises_str_val_is_not_prefix_of_str_param(self):
        s_ipo = IsPrefixOf(s_ipo='appy')
        with self.assertRaises(ValidationException) as context:
            s_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['sIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_int_is_not_prefix_of_list_param(self):
        loi_ipo = IsPrefixOf(loi_ipo=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            loi_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['loiIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_str_is_not_prefix_of_list_param(self):
        los_ipo = IsPrefixOf(los_ipo=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            los_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['losIpo'],
                         "prefix is not found")

    def test_is_prefix_of_validates_str_val_is_prefix_of_callable_param(self):
        c_ipo = IsPrefixOf(c_ipo='unha')
        c_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_int_is_prefix_of_callable_param(self):
        c_loi_ipo = IsPrefixOf(c_loi_ipo=[1, 4, 5])
        c_loi_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_str_is_prefix_of_callable_param(self):
        c_los_ipo = IsPrefixOf(c_los_ipo=['a', 'd'])
        c_los_ipo.validate()

    def test_is_prefix_of_raises_str_val_is_not_prefix_of_callable_param(self):
        c_ipo = IsPrefixOf(c_ipo='appy')
        with self.assertRaises(ValidationException) as context:
            c_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['cIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_int_is_not_prefix_of_callable_param(self):
        c_loi_ipo = IsPrefixOf(c_loi_ipo=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            c_loi_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['cLoiIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_str_is_not_prefix_of_callable_param(self):
        c_los_ipo = IsPrefixOf(c_los_ipo=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            c_los_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['cLosIpo'],
                         "prefix is not found")

    def test_is_prefix_of_validates_str_val_is_prefix_of_types_param(self):
        t_ipo = IsPrefixOf(t_ipo='unha')
        t_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_int_is_prefix_of_types_param(self):
        t_loi_ipo = IsPrefixOf(t_loi_ipo=[1, 4, 5])
        t_loi_ipo.validate()

    def test_is_prefix_of_validates_list_val_of_str_is_prefix_of_types_param(self):
        t_los_ipo = IsPrefixOf(t_los_ipo=['a', 'd'])
        t_los_ipo.validate()

    def test_is_prefix_of_raises_str_val_is_not_prefix_of_types_param(self):
        t_ipo = IsPrefixOf(t_ipo='appy')
        with self.assertRaises(ValidationException) as context:
            t_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['tIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_int_is_not_prefix_of_types_param(self):
        t_loi_ipo = IsPrefixOf(t_loi_ipo=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            t_loi_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['tLoiIpo'],
                         "prefix is not found")

    def test_is_prefix_of_raises_list_val_of_str_is_not_prefix_of_types_param(self):
        t_los_ipo = IsPrefixOf(t_los_ipo=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            t_los_ipo.validate()
        self.assertEqual(context.exception.keypath_messages['tLosIpo'],
                         "prefix is not found")
