"""module for dictof validator."""
from __future__ import annotations
from typing import Any
from inflection import underscore, camelize
from ..fields import FieldDescription, FieldType, Nullability
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class DictOfValidator(TypeValidator):
    """This validator validates dict."""

    def __init__(self, types: Any) -> None:
        self.cls = dict
        self.field_type = FieldType.DICT
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        super().define(field_description)
        field_description.dict_item_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        super().validate(context)
        types = resolve_types(self.types, context.config_owner.linked_class)
        if types.field_description.item_nullability == Nullability.UNDEFINED:
            types = types.required
        keypath_messages = {}
        for k, v in context.value.items():
            try:
                types.validator.validate(context.new(
                    value=v,
                    keypath_root=concat_keypath(context.keypath_root, k),
                    keypath_owner=concat_keypath(context.keypath_owner, k),
                    keypath_parent=k,
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
                value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        types = resolve_types(self.types, context.config_owner.linked_class)
        retval = {}
        for k, v in value.items():
            new_key = underscore(k) if context.config_owner.camelize_json_keys else k
            retval[new_key] = types.validator.transform(context.new(
                value=v,
                keypath_root=concat_keypath(context.keypath_root, new_key),
                keypath_owner=concat_keypath(context.keypath_owner, new_key),
                keypath_parent=new_key,
                parent=value,
                field_description=types.field_description))
        return retval

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if type(context.value) is not dict:
            return context.value
        types = resolve_types(self.types, context.config.linked_class)
        retval = {}
        for k, v in context.value.items():
            key = (camelize(k, False) if context.config.camelize_json_keys
                   else k)
            retval[key] = types.validator.tojson(context.new(value=v))
        return retval
