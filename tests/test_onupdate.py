from __future__ import annotations
from unittest import TestCase
from tests.classes.user_onupdate import (UserOnupdate, UserOnupdateD,
                                         UserOnupdateT, UserOnupdateZ,
                                         check_value, check_args)


class TestOnUpdate(TestCase):

    def test_onupdate_is_not_triggered_for_new_objects(self):
        val = check_value()
        user = UserOnupdate(name='A', age=20)
        user.age = 5
        user._set_on_save()
        self.assertEqual(check_value(), val)

    def test_onupdate_is_not_triggered_for_unmodified_fields(self):
        val = check_value()
        user = UserOnupdate(name='A', age=20)
        setattr(user, "_is_new", False)
        user.name = 'B'
        user._set_on_save()
        self.assertEqual(check_value(), val)

    def test_onupdate_is_triggered_for_modified_fields(self):
        val = check_value()
        user = UserOnupdate(name='A', age=20)
        setattr(user, "_is_new", False)
        user.age = 25
        user._set_on_save()
        self.assertEqual(check_value(), val + 1)
        self.assertEqual(check_args(), (-1, 25))

    def test_onupdate_accepts_two_args_old_and_new(self):
        val = check_value()
        user = UserOnupdateD(name='A', age=20)
        setattr(user, "_is_new", False)
        user.age = 25
        user._set_on_save()
        self.assertEqual(check_value(), val + 1)
        self.assertEqual(check_args(), (20, 25))

    def test_onupdate_accepts_three_args_old_new_and_context(self):
        val = check_value()
        user = UserOnupdateT(name='A', age=35)
        setattr(user, "_is_new", False)
        user.age = 45
        user._set_on_save()
        self.assertEqual(check_value(), val + 1)
        self.assertEqual(check_args(), (80, 90))

    def test_onupdate_accepts_zero_args(self):
        val = check_value()
        user = UserOnupdateZ(name='A', age=20)
        setattr(user, "_is_new", False)
        user.age = 25
        user._set_on_save()
        self.assertEqual(check_value(), val + 1)
        self.assertEqual(check_args(), (-50, -50))
