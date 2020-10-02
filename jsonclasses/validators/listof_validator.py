"""module for listof validator."""
from __future__ import annotations
from typing import Any
from ..fields import FieldDescription, FieldType, Nullability
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ListOfValidator(TypeValidator):
    """This validator validates list."""

    def __init__(self, types: Any) -> None:
        self.cls = list
        self.field_type = FieldType.LIST
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        super().define(field_description)
        field_description.list_item_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        super().validate(context)
        types = resolve_types(self.types, context.config_owner.linked_class)
        if types.field_description.item_nullability == Nullability.UNDEFINED:
            types = types.required
        keypath_messages = {}
        for i, v in enumerate(context.value):
            try:
                types.validator.validate(context.new(
                    value=v,
                    keypath_root=concat_keypath(context.keypath_root, i),
                    keypath_owner=concat_keypath(context.keypath_owner, i),
                    keypath_parent=i,
                    parent=context.value,
                    field_description=types.field_description))
            except ValidationException as exception:
                if context.all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages=keypath_messages, root=context.root)

    def transform(self, context: TransformingContext) -> Any:
        value = context.value
        fd = context.field_description
        assert fd is not None
        if fd.collection_nullability == Nullability.NONNULL:
            if value is None:
                value = []
        if context.value is None:
            return None
        if not isinstance(value, list):
            return value
        types = resolve_types(self.types, context.config_owner.linked_class)
        if types:
            retval = []
            for i, v in enumerate(value):
                transformed = types.validator.transform(context.new(
                    value=v,
                    keypath_root=concat_keypath(context.keypath_root, i),
                    keypath_owner=concat_keypath(context.keypath_owner, i),
                    keypath_parent=i,
                    parent=value,
                    field_description=types.field_description))
                retval.append(transformed)
            return retval
        else:
            return value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if type(context.value) is not list:
            return context.value
        types = resolve_types(self.types, context.config.linked_class)
        if types:
            retval = []
            for v in context.value:
                retval.append(types.validator.tojson(context.new(value=v)))
            return retval
        else:
            return context.value
