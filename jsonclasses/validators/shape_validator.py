"""module for shape validator."""
from typing import Dict, Any
from inflection import underscore, camelize
from ..fields import FieldDescription, FieldType, Nullability
from ..exceptions import ValidationException
from .validator import Validator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ShapeValidator(Validator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, types: Dict[str, Any]) -> None:
        if not isinstance(types, dict):
            raise ValueError('argument passed to ShapeValidator should be dict')
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.SHAPE
        field_description.shape_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if not isinstance(context.value, dict):
            raise ValidationException(
                {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be a dict.'},
                context.root
            )
        keypath_messages = {}
        for k, t in self.types.items():
            try:
                value_at_key = context.value[k]
            except KeyError:
                value_at_key = None
            types = resolve_types(t, context.config.linked_class)
            if types:
                try:
                    item_context = ValidatingContext(
                        value=value_at_key,
                        keypath=concat_keypath(context.keypath, k),
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
                value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        unused_keys = list(self.types.keys())
        retval = {}
        for k, field_value in value.items():
            new_key = underscore(k) if context.config.camelize_json_keys else k
            if new_key in unused_keys:
                t = self.types[new_key]
                types = resolve_types(t, context.config.linked_class)
                if types:
                    item_context = TransformingContext(
                        value=field_value,
                        keypath=concat_keypath(context.keypath, new_key),
                        root=context.root,
                        all_fields=context.all_fields,
                        config=context.config,
                        field_description=types.field_description)
                    retval[new_key] = types.validator.transform(item_context)
                else:
                    retval[new_key] = field_value
                unused_keys.remove(new_key)
        for k in unused_keys:
            retval[k] = None
        return retval

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if type(context.value) is not dict:
            return context.value
        retval = {}
        for k, t in self.types.items():
            key = camelize(k, False) if context.config.camelize_json_keys else k
            try:
                value_at_key = context.value[k]
            except KeyError:
                value_at_key = None
            types = resolve_types(t, context.config.linked_class)
            if types:
                item_context = ToJSONContext(
                    value=value_at_key,
                    config=context.config,
                    ignore_writeonly=context.ignore_writeonly)
                retval[key] = types.validator.tojson(item_context)
            else:
                retval[key] = value_at_key
        return retval
