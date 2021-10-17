from __future__ import annotations
from jsonclasses.excs import ValidationException
from tests.classes.super_prefix import SuperPrefix
from unittest import TestCase


class TestHasPrefix(TestCase):

    def test_hasprefix_validates_str_val_is_prefix_of_str_param(self):
        s_hp = SuperPrefix(s_hp='un')
        s_hp.validate()

    def test_hasprefix_validates_list_val_is_prefix_of_list_param_of_int(self):
        loi_hp = SuperPrefix(loi_hp=[1, 4, 5])
        loi_hp.validate()

    def test_hasprefix_validates_list_val_is_prefix_of_list_param_of_str(self):
        los_hp = SuperPrefix(los_hp=['a', 'd'])
        los_hp.validate()

    def test_hasprefix_raises_str_val_is_not_prefix_of_str_param(self):
        s_hp = SuperPrefix(s_hp='appy')
        with self.assertRaises(ValidationException) as context:
            s_hp.validate()
        self.assertEqual(context.exception.keypath_messages['sHp'],
                         "prefix is not found")

    def test_hasprefix_raises_list_val_is_not_prefix_of_list_param_of_int(self):
        loi_hp = SuperPrefix(loi_hp=[3, 2, 8])
        with self.assertRaises(ValidationException) as context:
            loi_hp.validate()
        self.assertEqual(context.exception.keypath_messages['loiHp'],
                         "prefix is not found")

    def test_hasprefix_raises_list_val_is_not_prefix_of_list_param_of_str(self):
            los_hp = SuperPrefix(los_hp=['f', 'g'])
            with self.assertRaises(ValidationException) as context:
                los_hp.validate()
            self.assertEqual(context.exception.keypath_messages['losHp'],
                            "prefix is not found")
