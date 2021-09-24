"""module for listof modifier."""
from __future__ import annotations
from typing import Any, Collection, Iterable
from ..fdef import FType
from .collection_type_modifier import CollectionTypeModifier


class ListOfModifier(CollectionTypeModifier):
    """This modifier validates list."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = list
        self.ftype = FType.LIST

    def enumerator(self, value: list) -> Iterable:
        return enumerate(value)

    def empty_collection(self) -> Collection:
        return []

    def append_value(self, i: int, v: Any, col: list):
        col.append(v)
