from __future__ import annotations
from typing import Generic, NamedTuple, TypeVar
from unittest import TestCase
from jsonclasses.owned_dict import OwnedDict

KT = TypeVar('KT')
VT = TypeVar('VT')


class AddRecord(NamedTuple):
    odict: OwnedDict
    key: KT
    val: VT


class DelRecord(NamedTuple):
    odict: OwnedDict
    val: VT


class Owner(Generic[KT, VT]):

    def __init__(self):
        self.add_records: list[AddRecord] = []
        self.del_records: list[DelRecord] = []

    def __odict_will_change__(self, olist: OwnedDict) -> None:
        pass

    def __odict_add__(self, odict: OwnedDict, key: KT, val: VT) -> None:
        self.add_records.append(AddRecord(odict, key, val))

    def __odict_del__(self, odict: OwnedDict, val: VT) -> None:
        self.del_records.append(DelRecord(odict, val))


class TestOwnedDict(TestCase):

    def test_owned_dict_get_notified_thru_clear(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.clear()
        self.assertEqual(owned_dict, {})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_dict, 2),
            DelRecord(owned_dict, 3)])

    def test_owned_dict_get_notified_thru_pop(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.pop('a')
        self.assertEqual(owned_dict, {'b': 3})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 2)])

    def test_owned_dict_get_notified_thru_pop_with_default(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.pop('a', 4)
        self.assertEqual(owned_dict, {'b': 3})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 2)])

    def test_owned_dict_get_notified_thru_pop_with_default_no_key(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.pop('z', 4)
        self.assertEqual(owned_dict, {'a': 2, 'b': 3})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [])

    def test_owned_dict_pop_undefined_key_raises(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(KeyError, 'z'):
            owned_dict.pop('z')

    def test_owned_dict_pop_zero_arguments_raises(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ('pop expected at least 1 '
                                                'argument, got 0')):
            owned_dict.pop()

    def test_owned_dict_pop_3_arguments_raises(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ('pop expected at most 2 '
                                                'arguments, got 3')):
            owned_dict.pop(1, 2, 3)

    def test_owned_dict_get_notified_thru_popitem(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.popitem()
        self.assertEqual(owned_dict, {'a': 2})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 3)])

    def test_owned_dict_get_notified_thru_setdefault(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.setdefault('c', 20)
        self.assertEqual(owned_dict, {'a': 2, 'b': 3, 'c': 20})
        self.assertEqual(owner.add_records, [AddRecord(owned_dict, 'c', 20)])
        self.assertEqual(owner.del_records, [])

    def test_owned_dict_get_notified_thru_setdefault_no_set(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 2, 'b': 3})
        owned_dict.owner = owner
        owned_dict.setdefault('a', 5)
        self.assertEqual(owned_dict, {'a': 2, 'b': 3})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [])

    def test_owned_dict_setdefault_3_arguments_raises(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ('setdefault expected at most 2'
                                                ' arguments, got 3')):
            owned_dict.setdefault(1, 2, 3)

    def test_owned_dict_setdefault_0_arguments_raises(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ('setdefault expected at least'
                                                ' 1 argument, got 0')):
            owned_dict.setdefault()

    def test_owned_dict_get_notified_thru_update_map(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        owned_dict.update({'c': 0, 'd': 4, 'e': 5})
        self.assertEqual(owned_dict, {'a': 1, 'b': 2, 'c': 0, 'd': 4, 'e': 5})
        self.assertEqual(owner.add_records, [
            AddRecord(owned_dict, 'c', 0),
            AddRecord(owned_dict, 'd', 4),
            AddRecord(owned_dict, 'e', 5)])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_dict, 3)])

    def test_owned_dict_get_notified_thru_update_iterable(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        owned_dict.update([('c', 0), ('d', 4), ('e', 5)])
        self.assertEqual(owned_dict, {'a': 1, 'b': 2, 'c': 0, 'd': 4, 'e': 5})
        self.assertEqual(owner.add_records, [
            AddRecord(owned_dict, 'c', 0),
            AddRecord(owned_dict, 'd', 4),
            AddRecord(owned_dict, 'e', 5)])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_dict, 3)])

    def test_owned_dict_get_notified_thru_update_map_and_kwargs(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        owned_dict.update({'c': 0, 'd': 4, 'e': 5}, c=7)
        self.assertEqual(owned_dict, {'a': 1, 'b': 2, 'c': 7, 'd': 4, 'e': 5})
        self.assertEqual(owner.add_records, [
            AddRecord(owned_dict, 'c', 7),
            AddRecord(owned_dict, 'd', 4),
            AddRecord(owned_dict, 'e', 5)])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_dict, 3)])

    def test_owned_dict_get_notified_thru_update_iterable_and_kwargs(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        owned_dict.update([('c', 0), ('d', 4), ('e', 5)], c=50)
        self.assertEqual(owned_dict, {'a': 1, 'b': 2, 'c': 50, 'd': 4, 'e': 5})
        self.assertEqual(owner.add_records, [
            AddRecord(owned_dict, 'c', 50),
            AddRecord(owned_dict, 'd', 4),
            AddRecord(owned_dict, 'e', 5)])
        self.assertEqual(owner.del_records, [
            DelRecord(owned_dict, 3)])

    def test_owned_dict_raises_when_wrong_arguments_to_update(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ('update expected at most 1 '
                                                'argument, got 2')):
            owned_dict.update([('c', 0), ('d', 4), ('e', 5)], {}, c=50)

    def test_owned_dict_raises_when_wrong_type_arguments_to_update(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, ("'int' object is not "
                                                "iterable")):
            owned_dict.update(5)

    def test_owned_dict_get_notified_thru_subscript_set_override(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2, 'c': 3})
        owned_dict.owner = owner
        owned_dict['a'] = 5
        self.assertEqual(owned_dict, {'a': 5, 'b': 2, 'c': 3})
        self.assertEqual(owner.add_records, [AddRecord(owned_dict, 'a', 5)])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 1)])

    def test_owned_dict_get_notified_thru_subscript_set_new(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2})
        owned_dict.owner = owner
        owned_dict['c'] = 3
        self.assertEqual(owned_dict, {'a': 1, 'b': 2, 'c': 3})
        self.assertEqual(owner.add_records, [AddRecord(owned_dict, 'c', 3)])
        self.assertEqual(owner.del_records, [])

    def test_owned_dict_get_notified_thru_subscript_del(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2})
        owned_dict.owner = owner
        del owned_dict['b']
        self.assertEqual(owned_dict, {'a': 1})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 2)])

    def test_owned_dict_raises_if_subscript_del_not_exist(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2})
        owned_dict.owner = owner
        with self.assertRaisesRegex(KeyError, 'q'):
            del owned_dict['q']
        self.assertEqual(owned_dict, {'a': 1, 'b': 2})
        self.assertEqual(owner.add_records, [])
        self.assertEqual(owner.del_records, [])

    def test_owned_dict_get_notified_thru_or_equal_sign(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2})
        owned_dict.owner = owner
        owned_dict |= {'b': 3, 'c': 4}
        self.assertEqual(owned_dict, {'a': 1, 'b': 3, 'c': 4})
        self.assertEqual(owner.add_records, [
            AddRecord(owned_dict, 'b', 3),
            AddRecord(owned_dict, 'c', 4)])
        self.assertEqual(owner.del_records, [DelRecord(owned_dict, 2)])

    def test_owned_dict_or_equal_sign_raises_if_wrong_argument(self):
        owner = Owner()
        owned_dict = OwnedDict({'a': 1, 'b': 2})
        owned_dict.owner = owner
        with self.assertRaisesRegex(TypeError, "'int' object is not iterable"):
            owned_dict |= 5
