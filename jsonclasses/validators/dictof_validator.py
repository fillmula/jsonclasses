"""module for dictof validator."""
from __future__ import annotations
from typing import Any, Iterable, Collection
from inflection import underscore, camelize
from ..field_definition import FieldType
from ..config import Config
from .collection_type_validator import CollectionTypeValidator


class DictOfValidator(CollectionTypeValidator):
    """This validator validates dict."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = dict
        self.field_type = FieldType.DICT

    def enumerator(self, value: dict[str, Any]) -> Iterable:
        return value.items()

    def empty_collection(self) -> Collection:
        return {}

    def append_value(self, i: str, v: Any, col: dict):
        col[i] = v

    def to_object_key(self, key: str, conf: Config) -> str:
        return underscore(key) if conf.camelize_json_keys else key

    def to_json_key(self, key: str, conf: Config) -> str:
        return camelize(key, False) if conf.camelize_json_keys else key
