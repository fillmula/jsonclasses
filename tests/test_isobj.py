from __future__ import annotations
from unittest import TestCase
from tests.classes.linked_permission import LinkedPermission, LinkedOwner
from jsonclasses.excs import UnauthorizedActionException


class TestIsObj(TestCase):

    def test_is_obj_is_valid_if_object_matches(self):
        owner2 = LinkedOwner(id='2')
        permission = LinkedPermission(owner=owner2)
        permission.opby(owner2)
        permission._can_read_check()
        owner1 = LinkedOwner(id='1')
        permission = LinkedPermission(owner=owner2)
        permission.opby(owner1)
        self.assertRaises(UnauthorizedActionException, permission._can_read_check)

    def test_is_obj_is_valid_if_object_id_matches_object(self):
        owner2 = LinkedOwner(id='2')
        permission = LinkedPermission(ownerId='2')
        permission.opby(owner2)
        permission._can_read_check()
        owner1 = LinkedOwner(id='1')
        permission = LinkedPermission(ownerId='2')
        permission.opby(owner1)
        self.assertRaises(UnauthorizedActionException, permission._can_read_check)
