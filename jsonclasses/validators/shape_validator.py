"""module for shape validator."""
from typing import Dict, Any
from inflection import underscore, camelize
from ..fields import FieldDescription, FieldType, Nullability, Strictness
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..utils.concat_keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class ShapeValidator(TypeValidator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, types: Dict[str, Any]) -> None:
        self.cls = dict
        self.field_type = FieldType.SHAPE
        self.types = types

    def define(self, field_description: FieldDescription) -> None:
        super().define(field_description)
        field_description.shape_types = self.types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        super().validate(context)
        keypath_messages = {}
        for k, t in self.types.items():
            try:
                value_at_key = context.value[k]
            except KeyError:
                value_at_key = None
            types = resolve_types(t, context.config_owner.linked_class)
            if types:
                try:
                    types.validator.validate(context.new(
                        value=value_at_key,
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
        unused_keys = list(self.types.keys())
        retval = {}
        for k, field_value in value.items():
            new_key = underscore(k) if context.config_owner.camelize_json_keys else k
            if new_key not in unused_keys:
                if fd.strictness == Strictness.STRICT:
                    raise ValidationException(
                        {context.keypath_root: f'Unallowed key \'{k}\' at \'{context.keypath_root}\'.'},
                        context.root)
                continue
            t = self.types[new_key]
            types = resolve_types(t, context.config_owner.linked_class)
            if types:
                retval[new_key] = types.validator.transform(context.new(
                    value=field_value,
                    keypath_root=concat_keypath(context.keypath_root, new_key),
                    keypath_owner=concat_keypath(context.keypath_owner, new_key),
                    keypath_parent=new_key,
                    parent=value,
                    field_description=types.field_description))
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
                retval[key] = types.validator.tojson(context.new(value=value_at_key))
            else:
                retval[key] = value_at_key
        return retval
