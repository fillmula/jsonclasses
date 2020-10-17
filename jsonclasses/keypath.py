"""This module contains keypath manipulation utilities."""
from typing import Union


def concat_keypath(*args: Union[str, int]):
    """Concatenate partial keypaths and keypath components into a concatenated
    keypath.
    """
    retval = ''
    for arg in args:
        if retval != '':
            retval += '.'
        retval += str(arg)
    return retval


def initial_keypaths(keypaths: set[str]) -> set[str]:
    """Keypaths can be connected with dots, return only initial.
    """
    retval = set()
    for keypath in keypaths:
        retval.add(keypath.split('.')[0])
    return retval
