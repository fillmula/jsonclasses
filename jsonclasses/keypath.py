"""This module defines utility functions for working with keypaths."""
from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING
from re import split,search
from .fdef import FStore, FType
if TYPE_CHECKING:
    from .jfield import JField


def raise_inflection_kindly():
    raise ModuleNotFoundError('please whether install inflection for the '
                              'default key encoding/decoding strategy '
                              'behavior or provide your own strategy')


def camelize_key(key: str) -> str:
    try:
        from inflection import camelize
    except ModuleNotFoundError as e:
        raise_inflection_kindly()
    return camelize(key, False)


def underscore_key(key: str) -> str:
    try:
        from inflection import underscore
    except ModuleNotFoundError as e:
        raise_inflection_kindly()
    return underscore(key)


def identical_key(key: str) -> str:
    return key


def reference_key(field: JField) -> str:
    """
    Figure out the correct reference key name from the field definition.

    Args:
        field (JField): The JSON class field to figure out reference
        key from.

    Returns:
        str: The reference key which represents this field.

    Raises:
        ValueError: ValueError is raised if the field definition is not a \
            supported reference field.
    """
    from inflection import singularize
    if field.fdef.fstore not in \
            [FStore.FOREIGN_KEY, FStore.LOCAL_KEY]:
        raise ValueError(f"field named {field.name} is not a reference field")
    if field.fdef.ftype == FType.LIST:
        return singularize(field.name) + '_ids'
    elif field.fdef.ftype == FType.INSTANCE:
        return field.name + '_id'
    else:
        raise ValueError(f"field type {field.fdef.ftype} is not a "
                         "supported reference field type")


def new_mongoid() -> str:
    from bson.objectid import ObjectId
    return str(ObjectId())


def concat_keypath(*args: Union[str, int]) -> str:
    """Concatenate partial keypaths and keys into a concatenated single
    keypath.

    Args:
        *args (Union[str, int]): The partial keypaths and keys to concatenate.

    Returns:
        str: the concatenated keypath.
    """
    return '.'.join([str(arg) for arg in args if len(str(arg)) > 0])


def keypath_drop_last(keypath: str) -> str:
    """Drop the last part of a keypath. If it only has one part, empty string
    is returned. If it's empty string, empty string is returned.

    Args:
        keypath (str): The keypath to drop last from.

    Returns:
        str: A new keypath with last component dropped or empty string.
    """
    return '.'.join(keypath.split('.')[:-1])


def initial_keypaths(keypaths: set[str]) -> set[str]:
    """Get a set of initial keypath component from `keypaths`.

    Args:
        keypaths (set[str]): A set of keypaths.

    Returns:
        set[str]: A set of initial keypath components without duplication.
    """
    return set([initial_keypath(k) for k in keypaths])


def initial_keypath(keypath: str) -> str:
    """Get the initial keypath component from the keypath.

    Args:
        keypath (str): The keypath to fetch the initial component from.

    Returns:
        str: The initial keypath component or empty string.
    """
    return keypath.split('.')[0]


def single_key_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if not search(r'\.|\[|\]', k)}


def compound_key_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if search(r'\.|\[|\]', k)}


def keypath_split(key: str) -> list[str]:
    return [k for k in split(r'\]|\[|\.', key) if len(k) > 0]
