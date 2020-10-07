from __future__ import annotations
from typing import Any, NamedTuple, List
from unittest import TestCase
from jsonclasses.owned_list import OwnedList


class AddRecord(NamedTuple):
    olist: OwnedList
    idx: int
    val: Any


class DelRecord(NamedTuple):
    olist: OwnedList
    val: Any


class SorRecord(NamedTuple):
    olist: OwnedList


class Owner:

    def __init__(self):
        self.add_records: List[AddRecord] = []
        self.del_records: List[DelRecord] = []
        self.sor_records: List[SorRecord] = []

    def __olist_add__(self, olist: OwnedList, index: int, val: Any) -> None:
        self.add_records.append(AddRecord(olist, index, val))

    def __olist_del__(self, olist: OwnedList, val: Any) -> None:
        self.del_records.append(DelRecord(olist, val))

    def __olist_sor__(self, olist: OwnedList) -> None:
        self.sor_records.append(SorRecord(olist))


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

    def test_owned_list_get_notified_thru_append(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        owned_list.append(4)
        self.assertEqual(owned_list, [1, 2, 3, 4])
        self.assertEqual(owner.add_records, [AddRecord(owned_list, 3, 4)])

    def test_owned_list_get_notified_thru_extend(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        owned_list.extend([4, 5])
        self.assertEqual(owned_list, [1, 2, 3, 4, 5])
        self.assertEqual(owner.add_records, [
            AddRecord(owned_list, 3, 4),
            AddRecord(owned_list, 4, 5)])

    def test_owned_list_get_notified_thru_insert(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        owned_list.insert(0, 0)
        self.assertEqual(owned_list, [0, 1, 2, 3])
        self.assertEqual(owner.add_records, [AddRecord(owned_list, 0, 0)])

    def test_owned_list_get_notified_thru_insert_idx_overflow(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        owned_list.insert(100, 0)
        self.assertEqual(owned_list, [1, 2, 3, 0])
        self.assertEqual(owner.add_records, [AddRecord(owned_list, 3, 0)])

    def test_owned_list_get_notified_thru_remove(self):
        owner = Owner()
        owned_list = OwnedList([1, 2, 3], owner)
        owned_list.remove(1)
        self.assertEqual(owned_list, [2, 3])
        self.assertEqual(owner.del_records, [DelRecord(owned_list, 1)])

    def test_owned_list_get_notified_thru_sort(self):
        owner = Owner()
        owned_list = OwnedList([1, 5, 3], owner)
        owned_list.sort()
        self.assertEqual(owned_list, [1, 3, 5])
        self.assertEqual(owner.sor_records, [SorRecord(owned_list)])

    def test_owned_list_get_notified_thru_clear(self):
        owner = Owner()
        owned_list = OwnedList([1, 5, 3], owner)
        owned_list.clear()
        self.assertEqual(owned_list, [])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_list, 1),
            DelRecord(owned_list, 5),
            DelRecord(owned_list, 3)])

    def test_owned_list_get_notified_thru_pop(self):
        owner = Owner()
        owned_list = OwnedList([1, 5, 3], owner)
        owned_list.pop()
        self.assertEqual(owned_list, [1, 5])
        self.assertEqual(owner.del_records, [DelRecord(owned_list, 3)])

    def test_owned_list_get_notified_thru_pop_argument(self):
        owner = Owner()
        owned_list = OwnedList([1, 5, 3], owner)
        owned_list.pop(0)
        self.assertEqual(owned_list, [5, 3])
        self.assertEqual(owner.del_records, [DelRecord(owned_list, 1)])

    def test_owned_list_get_notified_thru_reverse(self):
        owner = Owner()
        owned_list = OwnedList([1, 5, 3], owner)
        owned_list.reverse()
        self.assertEqual(owned_list, [3, 5, 1])
        self.assertEqual(owner.sor_records, [SorRecord(owned_list)])
