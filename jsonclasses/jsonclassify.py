"""This module defines the `jsonclassify` function."""
from __future__ import annotations


def __init__(self):
    print("ok", self)


def ok(self):
    print(self.val)


def jsonclassify(cls: type) -> type:
    cls.ok = ok
    cls.__init__ = __init__
    return cls
