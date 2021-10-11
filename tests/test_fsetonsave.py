from __future__ import annotations
from unittest import TestCase
from tests.classes.user_sos import UserFSOS


class TestFSetOnSave(TestCase):

    def test_unmodified_object_still_triggers_setonsave(self):
        user = UserFSOS(name='n')
        setattr(user, '_is_new', False)
        user._set_on_save()
        self.assertEqual(user.age, 100)
        user._set_on_save()
        self.assertEqual(user.age, 200)
