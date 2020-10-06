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
