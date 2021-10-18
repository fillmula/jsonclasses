from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_prefix import SuperPrefix
from unittest import TestCase


class TestHasPrefix(TestCase):

    def test_hasprefix_validates_a_str_is_prefix_of_original_str(self):
        s_hp = SuperPrefix(s_hp='unsasf')
        s_hp.validate()

    def test_hasprefix_validates_list_param_is_prefix_of_list_val_of_int(self):
        loi_hp = SuperPrefix(loi_hp=[1, 4, 5])
        loi_hp.validate()

    def test_hasprefix_validates_list_param_is_prefix_of_list_val_of_str(self):
        los_hp = SuperPrefix(los_hp=['a', 'd'])
        los_hp.validate()

    def test_hasprefix_raises_str_param_is_not_prefix_of_str_val(self):
        s_hp = SuperPrefix(s_hp='appy')
        with self.assertRaises(ValidationException) as context:
            s_hp.validate()
        self.assertEqual(context.exception.keypath_messages['sHp'],
                         "prefix is not found")

    def test_hasprefix_raises_list_param_is_not_prefix_of_list_val_of_int(self):
        loi_hp = SuperPrefix(loi_hp=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            loi_hp.validate()
        self.assertEqual(context.exception.keypath_messages['loiHp'],
                         "prefix is not found")

    def test_hasprefix_raises_list_param_is_not_prefix_of_list_val_of_str(self):
            los_hp = SuperPrefix(los_hp=['f', 'g'])
            with self.assertRaises(ValidationException) as context:
                los_hp.validate()
            self.assertEqual(context.exception.keypath_messages['losHp'],
                            "prefix is not found")

    def test_hasprefix_validates_callable_param_is_prefix_of_str_val(self):
        c_hp = SuperPrefix(c_hp='un')
        c_hp.validate()

    def test_hasprefix_validates_callable_param_is_prefix_of_list_val_of_int(self):
        c_loi_hp = SuperPrefix(c_loi_hp=[1, 4, 5])
        c_loi_hp.validate()

    def test_hasprefix_validates_callable_param_is_prefix_of_list_val_of_str(self):
        c_los_hp = SuperPrefix(c_los_hp=['a', 'd'])
        c_los_hp.validate()

    def test_hasprefix_raises_callable_param_is_not_prefix_of_str_val(self):
        c_hp = SuperPrefix(c_hp='appy')
        with self.assertRaises(ValidationException) as context:
            c_hp.validate()
        self.assertEqual(context.exception.keypath_messages['cHp'],
                         "prefix is not found")

    def test_hasprefix_raises_callable_param_is_not_prefix_of_list_val_of_int(self):
        c_loi_hp = SuperPrefix(c_loi_hp=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            c_loi_hp.validate()
        self.assertEqual(context.exception.keypath_messages['cLoiHp'],
                         "prefix is not found")

    def test_hasprefix_raises_callable_param_is_not_prefix_of_list_val_of_str(self):
        c_los_hp = SuperPrefix(c_los_hp=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            c_los_hp.validate()
        self.assertEqual(context.exception.keypath_messages['cLosHp'],
                        "prefix is not found")

    def test_hasprefix_validates_types_param_is_prefix_of_str_val(self):
        t_hp = SuperPrefix(t_hp='un')
        t_hp.validate()

    def test_hasprefix_validates_types_param_is_prefix_of_list_val_of_int(self):
        t_loi_hp = SuperPrefix(t_loi_hp=[1, 4, 5])
        t_loi_hp.validate()

    def test_hasprefix_validates_types_param_is_prefix_of_list_val_of_str(self):
        t_los_hp = SuperPrefix(t_los_hp=['a', 'd'])
        t_los_hp.validate()

    def test_hasprefix_raises_types_param_is_not_prefix_of_str_val(self):
        t_hp = SuperPrefix(t_hp='appy')
        with self.assertRaises(ValidationException) as context:
            t_hp.validate()
        self.assertEqual(context.exception.keypath_messages['tHp'],
                         "prefix is not found")

    def test_hasprefix_raises_types_param_is_not_prefix_of_list_val_of_int(self):
        t_loi_hp = SuperPrefix(t_loi_hp=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            t_loi_hp.validate()
        self.assertEqual(context.exception.keypath_messages['tLoiHp'],
                         "prefix is not found")

    def test_hasprefix_raises_types_param_is_not_prefix_of_list_val_of_str(self):
        t_los_hp = SuperPrefix(t_los_hp=['f', 'g'])
        with self.assertRaises(ValidationException) as context:
            t_los_hp.validate()
        self.assertEqual(context.exception.keypath_messages['tLosHp'],
                        "prefix is not found")
