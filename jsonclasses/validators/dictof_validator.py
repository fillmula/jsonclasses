"""module for dictof validator."""
from __future__ import annotations
from typing import Any, Iterable, Collection
from inflection import underscore, camelize
from ..fields import FieldType, Nullability
from .collection_type_validator import CollectionTypeValidator
from ..keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import TransformingContext, ToJSONContext


class DictOfValidator(CollectionTypeValidator):
    """This validator validates dict."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = dict
        self.field_type = FieldType.DICT

    def enumerator(self, value: dict[str, Any]) -> Iterable:
        return value.items()

    def empty_value(self) -> Collection:
        return {}

    def append_value(self, i: str, v: Any, col: dict):
        col[i] = v

    def transform(self, context: TransformingContext) -> Any:
        value = context.value
        fd = context.fdesc
        assert fd is not None
        if fd.collection_nullability == Nullability.NONNULL:
            if value is None:
                value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        types = resolve_types(self.raw_item_types, context.config_owner.linked_class)
        retval = {}
        for k, v in value.items():
            new_key = underscore(k) if context.config_owner.camelize_json_keys else k
            retval[new_key] = types.validator.transform(context.new(
                value=v,
                keypath_root=concat_keypath(context.keypath_root, new_key),
                keypath_owner=concat_keypath(context.keypath_owner, new_key),
                keypath_parent=new_key,
                parent=value,
                fdesc=types.fdesc))
        return retval

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, dict):
            return context.value
        types = resolve_types(self.raw_item_types, context.config.linked_class)
        retval = {}
        for k, v in context.value.items():
            key = (camelize(k, False) if context.config.camelize_json_keys
                   else k)
            retval[key] = types.validator.tojson(context.new(value=v))
        return retval
