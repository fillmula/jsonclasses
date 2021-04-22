from __future__ import annotations
from unittest import TestCase
from tests.classes.user_onsave import (UserOnsave, UserOnsaveZ, check_value,
                                       check_args)


class TestOnSave(TestCase):

    def test_onsave_is_triggered_for_new_objects(self):
        val = check_value()
        user = UserOnsave(name='Lao', age=6)
        user.name = 'Ua Tsiu Liong Bo Ho'
        user._set_on_save()
        self.assertEqual(val + 1, check_value())
        self.assertEqual(check_args(), 6)

    def test_onsave_is_triggered_for_modified_objects(self):
        val = check_value()
        user = UserOnsave(name='Lao', age=7)
        setattr(user, '_is_new', False)
        user.name = 'Ua Tsiu Liong Bo Ho'
        user._set_on_save()
        self.assertEqual(val + 1, check_value())
        self.assertEqual(check_args(), 7)

    def test_onsave_is_not_triggered_for_unmodified_objects(self):
        val = check_value()
        user = UserOnsave(name='Lao', age=5)
        setattr(user, '_is_new', False)
        user._set_on_save()
        self.assertEqual(val, check_value())
        self.assertNotEqual(check_args(), 5)

    def test_onsave_can_take_no_args(self):
        val = check_value()
        user = UserOnsaveZ(name='Cong Ti', age=10)
        setattr(user, '_is_new', False)
        user.name = 'Mai Kah Ua Cong Kha'
        user._set_on_save()
        self.assertEqual(val + 10, check_value())
        self.assertNotEqual(check_args(), 10)
