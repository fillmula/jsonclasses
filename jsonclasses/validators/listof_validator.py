"""module for listof validator."""
from __future__ import annotations
from typing import Any, Collection, Iterable
from ..fields import FieldType, Nullability
from .collection_type_validator import CollectionTypeValidator
from ..keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import TransformingContext, ToJSONContext


class ListOfValidator(CollectionTypeValidator):
    """This validator validates list."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = list
        self.field_type = FieldType.LIST

    def enumerator(self, value: list) -> Iterable:
        return enumerate(value)

    def empty_value(self) -> Collection:
        return []

    def append_value(self, i: int, v: Any, col: list):
        col.append(v)
