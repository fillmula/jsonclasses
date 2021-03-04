from __future__ import annotations
from typing import Any


def isjsonclass(class_: type) -> bool:
    """Check if a class is jsonclass.

    Args:
        class_ (type): The class to check.

    Returns:
        bool: True if it's a jsonclass, otherwise False.
    """
    return hasattr(class_, '__is_jsonclass__')


def isjsonobject(object: Any) -> bool:
    """Check if an object is instance of jsonclass.

    Args:
        object (Any): The object to check.

    Returns:
        bool: True if it's an instance of jsonclass otherwise False.
    """
    return isjsonclass(object.__class__)
