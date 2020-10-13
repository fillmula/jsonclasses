"""module for listof validator."""
from __future__ import annotations
from typing import Any
from ..fields import FieldDescription, FieldType, Nullability
from ..exceptions import ValidationException
from .collection_type_validator import CollectionTypeValidator
from ..keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ListOfValidator(CollectionTypeValidator):
    """This validator validates list."""

    def __init__(self, raw_item_types: Any) -> None:
        super().__init__(raw_item_types)
        self.cls = list
        self.field_type = FieldType.LIST

    def transform(self, context: TransformingContext) -> Any:
        value = context.value
        fd = context.fdesc
        assert fd is not None
        if fd.collection_nullability == Nullability.NONNULL:
            if value is None:
                value = []
        if value is None:
            return None
        if not isinstance(value, list):
            return value
        types = resolve_types(self.raw_item_types, context.config_owner.linked_class)
        if types:
            retval = []
            for i, v in enumerate(value):
                transformed = types.validator.transform(context.new(
                    value=v,
                    keypath_root=concat_keypath(context.keypath_root, i),
                    keypath_owner=concat_keypath(context.keypath_owner, i),
                    keypath_parent=i,
                    parent=value,
                    fdesc=types.fdesc))
                retval.append(transformed)
            return retval
        else:
            return value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, list):
            return context.value
        types = resolve_types(self.raw_item_types, context.config.linked_class)
        if types:
            retval = []
            for v in context.value:
                retval.append(types.validator.tojson(context.new(value=v)))
            return retval
        else:
            return context.value
