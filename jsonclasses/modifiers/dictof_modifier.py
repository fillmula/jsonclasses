"""module for dictof modifier."""
from __future__ import annotations
from typing import Any, Iterable, Collection
from ..fdef import FType
from ..jconf import JConf
from .collection_type_modifier import CollectionTypeModifier


class DictOfModifier(CollectionTypeModifier):
    """This modifier validates dict."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = dict
        self.ftype = FType.DICT

    def enumerator(self, value: dict[str, Any]) -> Iterable:
        return value.items()

    def empty_collection(self) -> Collection:
        return {}

    def append_value(self, i: str, v: Any, col: dict):
        col[i] = v

    def to_object_key(self, key: str, conf: JConf) -> str:
        return key

    def to_json_key(self, key: str, conf: JConf) -> str:
        return key
