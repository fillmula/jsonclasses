"""This module contains utility methods for working with owned collections.
"""
from __future__ import annotations
from typing import TypeVar, Any
from .owned_dict import OwnedDict, DictOwner
from .owned_list import OwnedList, ListOwner
from .keypath_utils import concat_keypath

KT = TypeVar('KT')
VT = TypeVar('VT')
T = TypeVar('T')


def to_owned_dict(owner: DictOwner,
                  dct: dict[KT, VT],
                  keypath: str) -> OwnedDict[KT, VT]:
    new_dct = {}
    for k, v in dct.items():
        if isinstance(v, list):
            new_dct[k] = to_owned_list(owner, v, concat_keypath(keypath, k))
        elif isinstance(v, dict):
            new_dct[k] = to_owned_dict(owner, v, concat_keypath(keypath, k))
        else:
            new_dct[k] = v
    owned_dict = OwnedDict[Any](new_dct)
    owned_dict.keypath = keypath
    owned_dict.owner = owner
    return owned_dict


def to_owned_list(owner: ListOwner,
                  lst: list[T],
                  keypath: str) -> OwnedList[T]:
    new_lst = []
    for i, v in enumerate(lst):
        if isinstance(v, list):
            new_lst.append(to_owned_list(owner, v, concat_keypath(keypath, i)))
        elif isinstance(v, dict):
            new_lst.append(to_owned_dict(owner, v, concat_keypath(keypath, i)))
        else:
            new_lst.append(v)
    owned_list = OwnedList[Any](new_lst)
    owned_list.keypath = keypath
    owned_list.owner = owner
    return owned_list


def unowned_copy_dict(any_dict: dict[KT, VT]) -> dict[KT, VT]:
    retval = {}
    for k, v in any_dict.items():
        if isinstance(v, dict):
            retval[k] = unowned_copy_dict(v)
        elif isinstance(v, list):
            retval[k] = unowned_copy_list(v)
        else:
            retval[k] = v
    return retval


def unowned_copy_list(any_list: list[T]) -> list[T]:
    retval = []
    for v in any_list:
        if isinstance(v, dict):
            retval.append(unowned_copy_dict(v))
        elif isinstance(v, list):
            retval.append(unowned_copy_list(v))
        else:
            retval.append(v)
    return retval
