from __future__ import annotations
from unittest import TestCase
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser


class TestSerialize(TestCase):

    def test_serialize_linked_objects_wont_go_into_infinite_loop(self):
        profile = LinkedProfile(name='Ua Bê Tshiu Pên')
        user = LinkedUser(name='Tsuan Sê Kai')
        user.profile = profile
        user._set_on_save()
