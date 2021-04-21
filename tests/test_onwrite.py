from __future__ import annotations
from unittest import TestCase
from tests.classes.onwrite import (OnwriteSingle, OnwriteDouble, OnwriteTriple,
                                   check_value)


class TestOnWrite(TestCase):

    def test_new_object_triggers_onwrite(self):
        val = check_value()
        item = OnwriteSingle(a='a', b=1)
        item.a = 'b'
        item._set_on_save()
        self.assertEqual(val + 1, check_value())

    def test_exist_object_wont_trigger_if_this_field_is_not_modified(self):
        val = check_value()
        item = OnwriteSingle(a='a', b=1)
        setattr(item, '_is_new', False)
        item.a = 'b'
        item._set_on_save()
        self.assertEqual(val, check_value())

    def test_exist_object_triggers_if_this_field_is_modified(self):
        val = check_value()
        item = OnwriteSingle(a='a', b=1)
        setattr(item, '_is_new', False)
        item.b = 5
        item._set_on_save()
        self.assertEqual(val + 1, check_value())

    def test_onwrite_accepts_value(self):
        val = check_value()
        item = OnwriteDouble(a='a', b=1)
        setattr(item, '_is_new', False)
        item.b = 5
        item._set_on_save()
        self.assertEqual(val + 5, check_value())

    def test_onwrite_accepts_value_and_context(self):
        val = check_value()
        item = OnwriteTriple(a='a', b=1)
        setattr(item, '_is_new', False)
        item.b = 5
        item._set_on_save()
        self.assertEqual(val + 10, check_value())
