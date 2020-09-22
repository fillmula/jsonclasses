"""module for listof validator."""
from __future__ import annotations
from typing import Any
from ..fields import FieldDescription, FieldType, Nullability
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ListOfValidator(Validator):
    """This validator validates list."""

    def __init__(self, types: Any) -> None:
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.LIST
        field_description.list_item_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if type(context.value) is not list:
            raise ValidationException(
                {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be a list.'},
                context.root
            )
        types = resolve_types(self.types, context.config.linked_class)
        if types:
            if types.field_description.item_nullability == Nullability.UNDEFINED:
                types = types.required
            keypath_messages = {}
            for i, v in enumerate(context.value):
                try:
                    item_context = ValidatingContext(
                        value=v,
                        keypath=concat_keypath(context.keypath, i),
                        root=context.root,
                        all_fields=context.all_fields,
                        config=context.config,
                        field_description=types.field_description)
                    types.validator.validate(item_context)
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
        if fd.collection_nullability == Nullability.NONNULL:
            if value is None:
                value = []
        if context.value is None:
            return None
        if not isinstance(value, list):
            return value
        types = resolve_types(self.types, context.config.linked_class)
        if types:
            retval = []
            for i, v in enumerate(value):
                item_context = TransformingContext(
                    value=v,
                    keypath=concat_keypath(context.keypath, i),
                    root=context.root,
                    all_fields=context.all_fields,
                    config=context.config,
                    field_description=types.field_description)
                transformed = types.validator.transform(item_context)
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
                item_context = ToJSONContext(
                    value=v,
                    config=context.config,
                    ignore_writeonly=context.ignore_writeonly)
                retval.append(types.validator.tojson(item_context))
            return retval
        else:
            return context.value
