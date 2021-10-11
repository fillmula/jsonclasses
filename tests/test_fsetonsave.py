from __future__ import annotations
from unittest import TestCase
from tests.classes.user_sos import UserFSOS, UserTFSOS


class TestFSetOnSave(TestCase):

    def test_unmodified_object_still_triggers_fsetonsave_func_setter(self):
        user = UserFSOS(name='n')
        setattr(user, '_is_new', False)
        user._set_on_save()
        self.assertEqual(user.age, 100)
        user._set_on_save()
        self.assertEqual(user.age, 200)

    def test_unmodified_object_still_triggers_fsetonsave_types_setter(self):
        user = UserTFSOS(name='n')
        setattr(user, '_is_new', False)
        user._set_on_save()
        code1 = user.code
        user._set_on_save()
        code2 = user.code
        self.assertNotEqual(code1, code2)
        self.assertRegex(code1, '\d{4}')
        self.assertRegex(code2, '\d{4}')
