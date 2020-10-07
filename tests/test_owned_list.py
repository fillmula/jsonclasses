from __future__ import annotations
from typing import Any
from unittest import TestCase
from jsonclasses.owned_list import OwnedList


class Owner:

    def __init__(self):
        self.add_map = {}
        self.del_map = {}

    def __olist_add__(self, olist: OwnedList, val: Any, index: int) -> None:
        self.add_map[str(index)] = val

    def __olist_del__(self, olist: OwnedList, val: Any, index: int) -> None:
        self.del_map[str(index)] = val


class TestOwnedList(TestCase):

    def test_owned_list_can_be_created_with_owner_arg(self):
        owner = Owner()
        owned_list = OwnedList(owner)
        self.assertEqual(owned_list, [])
        self.assertEqual(owned_list.__class__, OwnedList)
        self.assertEqual(owned_list.owner, owner)

    def test_owned_list_can_be_created_with_owner_kwarg(self):
        owner = Owner()
        owned_list = OwnedList(owner=owner)
        self.assertEqual(owned_list, [])
        self.assertEqual(owned_list.__class__, OwnedList)
        self.assertEqual(owned_list.owner, owner)

    def test_owned_list_can_be_created_with_owner_and_iterable_arg(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        self.assertEqual(owned_list, [1, 2, 3])
        self.assertEqual(owned_list.__class__, OwnedList)
        self.assertEqual(owned_list.owner, owner)

    def test_owned_list_can_be_created_with_owner_and_iterable_kwarg(self):
        owner = Owner()
        owned_list = OwnedList(iterable=[1, 2, 3], owner=owner)
        self.assertEqual(owned_list, [1, 2, 3])
        self.assertEqual(owned_list.__class__, OwnedList)
        self.assertEqual(owned_list.owner, owner)
