"""This module contains keypath manipulation utilities."""
from typing import Union


def concat_keypath(*args: Union[str, int]) -> str:
    """Concatenate partial keypaths and keypath components into a concatenated
    keypath.
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
    """
    if keypath == '':
        return ''
    parts = keypath.split('.')
    parts.pop()
    return '.'.join(parts)


def initial_keypaths(keypaths: set[str]) -> set[str]:
    """Keypaths can be connected with dots, return only initial.
    """
    retval = set()
    for keypath in keypaths:
        retval.add(initial_keypath(keypath))
    return retval


def initial_keypath(keypath: str) -> str:
    """Returns the initial keypath item from the keypath.
    """
    return keypath.split('.')[0]
