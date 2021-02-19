"""This module contains utility methods for deep copying owned container types
into plain types.
"""
from __future__ import annotations
from typing import TypeVar

KT = TypeVar('KT')
VT = TypeVar('VT')
T = TypeVar('T')


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
