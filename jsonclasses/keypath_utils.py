"""This module defines utility functions for working with keypaths."""
from __future__ import annotations
from typing import Union, TYPE_CHECKING
from .field_definition import FieldStorage, FieldType
if TYPE_CHECKING:
    from .jsonclass_field import JSONClassField


def reference_key(field: JSONClassField) -> str:
    """
    Figure out the correct reference key name from the field definition.

    Args:
        field (JSONClassField): The JSON class field to figure out reference
        key from.

    Returns:
        str: The reference key which represents this field.

    Raises:
        ValueError: ValueError is raised if the field definition is not a \
            supported reference field.
    """
    if field.definition.field_storage not in \
            [FieldStorage.FOREIGN_KEY, FieldStorage.LOCAL_KEY]:
        raise ValueError(f"field named {field.name} is not a reference field")
    if field.definition.field_type == FieldType.LIST:
        return field.name + '_ids'
    elif field.definition.field_type == FieldType.INSTANCE:
        return field.name + '_id'
    else:
        raise ValueError(f"field type {field.definition.field_type} is not a "
                         "supported reference field type")


def concat_keypath(*args: Union[str, int]) -> str:
    """Concatenate partial keypaths and keys into a concatenated single
    keypath.

    Args:
        *args (Union[str, int]): The partial keypaths and keys to concatenate.

    Returns:
        str: the concatenated keypath.
    """
    retval = ''
    for arg in args:
        if retval != '':
            retval += '.'
        retval += str(arg)
    return retval


def keypath_drop_last(keypath: str) -> str:
    """Drop the last part of a keypath. If it only has one part, empty string
    is returned. If it's empty string, empty string is returned.

    Args:
        keypath (str): The keypath to drop last from.

    Returns:
        str: A new keypath with last component dropped or empty string.
    """
    if keypath == '':
        return ''
    parts = keypath.split('.')
    parts.pop()
    return '.'.join(parts)


def initial_keypaths(keypaths: set[str]) -> set[str]:
    """Get a set of initial keypath component from `keypaths`.

    Args:
        keypaths (set[str]): A set of keypaths.

    Returns:
        set[str]: A set of initial keypath components without duplication.
    """
    retval = set()
    for keypath in keypaths:
        retval.add(initial_keypath(keypath))
    return retval


def initial_keypath(keypath: str) -> str:
    """Get the initial keypath component from the keypath.

    Args:
        keypath (str): The keypath to fetch the initial component from.

    Returns:
        str: The initial keypath component or empty string.
    """
    return keypath.split('.')[0]
