"""module for shape validator."""
from typing import Any, Sequence, cast
from inflection import underscore, camelize
from ..fields import FieldDescription, FieldType, Nullability, Strictness
from ..exceptions import ValidationException
from ..config import Config
from ..keypath import concat_keypath
from ..types_resolver import resolve_types
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext
from .type_validator import TypeValidator


class ShapeValidator(TypeValidator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, shape_types: dict[str, Any]) -> None:
        super().__init__()
        self.cls = dict
        self.field_type = FieldType.SHAPE
        self.shape_types = shape_types
        self.exact_type = False

    def define(self, fdesc: FieldDescription) -> None:
        super().define(fdesc)
        fdesc.shape_types = self.shape_types

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        super().validate(context)
        all_fields = context.all_fields
        if all_fields is None:
            all_fields = context.config_owner.validate_all_fields
        keypath_messages = {}
        for k, t in self.shape_types.items():
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
                        fdesc=types.fdesc))
                except ValidationException as exception:
                    if all_fields:
                        keypath_messages.update(exception.keypath_messages)
                    else:
                        raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages, root=context.root)

    def _has_field_value(self,
                         field_key: str,
                         keys: Sequence[str],
                         config: Config) -> bool:
        field_name = field_key
        json_field_name = field_name
        if config.camelize_json_keys:
            json_field_name = camelize(field_name, False)
        return json_field_name in keys or field_name in keys

    def _get_field_value(self,
                         field_key: str,
                         value: dict[str, Any],
                         config: Config) -> Any:
        field_value = value.get(field_key)
        if field_value is None and config.camelize_json_keys:
            field_value = value.get(camelize(field_key, False))
        return field_value

    def _strictness_check(self,
                          value: dict[str, Any],
                          context: TransformingContext):
        value_keys = list(value.keys())
        if context.config_owner.camelize_json_keys:
            value_keys = [underscore(k) for k in value_keys]
        keys = self.shape_types.keys()
        for k in value_keys:
            if k not in keys:
                raise ValidationException(
                    {context.keypath_root: (f'Unallowed key \'{k}\' at '
                                            f'\'{context.keypath_root}\'.')},
                    context.root)

    def transform(self, context: TransformingContext) -> Any:
        value = context.value
        fd = cast(FieldDescription, context.fdesc)
        if fd.collection_nullability == Nullability.NONNULL and value is None:
            value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        if fd.strictness == Strictness.STRICT:
            self._strictness_check(value, context)
        retval = {}
        for fk, ft in self.shape_types.items():
            fv = None
            if self._has_field_value(fk,
                                     list(value.keys()),
                                     context.config_owner):
                fv = self._get_field_value(fk, value, context.config_owner)
            types = resolve_types(ft, context.config_owner.linked_class)
            retval[fk] = types.validator.transform(context.new(
                value=fv,
                keypath_root=concat_keypath(context.keypath_root, fk),
                keypath_owner=concat_keypath(context.keypath_owner, fk),
                keypath_parent=fk,
                parent=value,
                fdesc=types.fdesc))
        return retval

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, dict):
            return context.value
        retval = {}
        for k, t in self.shape_types.items():
            key = camelize(k, False) if context.config.camelize_json_keys else k
            value_at_key = context.value.get(k)
            types = resolve_types(t, context.config.linked_class)
            if types:
                retval[key] = types.validator.tojson(context.new(value=value_at_key))
            else:
                retval[key] = value_at_key
        return retval

    def serialize(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, dict):
            return context.value
        retval = {}
        for key, raw_types in self.shape_types.items():
            value_at_key = context.value.get(key)
            types = resolve_types(raw_types, context.config.linked_class)
            if types:
                retval[key] = types.validator.transform(context.new(
                    value=value_at_key,
                    keypath_root=concat_keypath(context.keypath_root, key),
                    keypath_owner=concat_keypath(context.keypath_owner, key),
                    keypath_parent=key,
                    parent=context.value,
                    fdesc=types.fdesc))
            else:
                retval[key] = value_at_key
        return retval
