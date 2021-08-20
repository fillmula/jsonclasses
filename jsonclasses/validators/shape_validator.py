"""module for shape validator."""
from typing import Any, Sequence, Union, cast
from inflection import underscore, camelize
from ..fdef import Fdef, FieldType, Nullability, Strictness
from ..exceptions import ValidationException
from ..jconf import JConf
from ..keypath import concat_keypath
from ..rtypes import rtypes
from ..ctxs import VCtx, TCtx, JCtx
from .type_validator import TypeValidator


class ShapeValidator(TypeValidator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, raw_shape_types: Union[dict[str, Any], str, type]) -> None:
        super().__init__()
        self.cls = dict
        self.field_type = FieldType.SHAPE
        self.raw_types = raw_shape_types
        self.exact_type = False

    def raw_shape_types(self, owner_cls: type) -> dict[str, Any]:
        if hasattr(self, '_raw_shape_types'):
            return getattr(self, '_raw_shape_types')
        else:
            if isinstance(self.raw_types, dict):
                setattr(self, '_raw_shape_types', self.raw_types)
                return self._raw_shape_types
            itypes = rtypes(self.raw_types, owner_cls)
            if itypes.fdef.item_nullability == Nullability.UNDEFINED:
                itypes = itypes.required
            stypes = itypes.fdef.raw_shape_types
            setattr(self, '_raw_shape_types', stypes)
            return stypes

    def define(self, fdef: Fdef) -> None:
        super().define(fdef)
        fdef._raw_shape_types = self.raw_types

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return
        super().validate(context)
        all_fields = context.all_fields
        if all_fields is None:
            all_fields = context.jconf_owner.validate_all_fields
        keypath_messages = {}
        for k, t in self.raw_shape_types(context.jconf_owner.cls).items():
            try:
                value_at_key = context.value[k]
            except KeyError:
                value_at_key = None
            types = rtypes(t, context.jconf_owner)
            if types:
                try:
                    types.validator.validate(context.new(
                        value=value_at_key,
                        keypath_root=concat_keypath(context.keypath_root, k),
                        keypath_owner=concat_keypath(context.keypath_owner, k),
                        keypath_parent=k,
                        parent=context.value,
                        fdef=types.fdef))
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
                         jconf: JConf) -> bool:
        field_name = field_key
        json_field_name = field_name
        if jconf.camelize_json_keys:
            json_field_name = camelize(field_name, False)
        return json_field_name in keys or field_name in keys

    def _get_field_value(self,
                         field_key: str,
                         value: dict[str, Any],
                         jconf: JConf) -> Any:
        field_value = value.get(field_key)
        if field_value is None and jconf.camelize_json_keys:
            field_value = value.get(camelize(field_key, False))
        return field_value

    def _strictness_check(self,
                          value: dict[str, Any],
                          context: TCtx):
        value_keys = list(value.keys())
        if context.jconf_owner.camelize_json_keys:
            value_keys = [underscore(k) for k in value_keys]
        keys = self.raw_shape_types(context.jconf_owner.cls).keys()
        for k in value_keys:
            if k not in keys:
                raise ValidationException(
                    {context.keypath_root: (f'Unallowed key \'{k}\' at '
                                            f'\'{context.keypath_root}\'.')},
                    context.root)

    def transform(self, context: TCtx) -> Any:
        value = context.value
        fd = cast(Fdef, context.fdef)
        if fd.collection_nullability == Nullability.NONNULL and value is None:
            value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        if fd.strictness == Strictness.STRICT:
            self._strictness_check(value, context)
        retval = {}
        for fk, ft in self.raw_shape_types(context.jconf_owner.cls).items():
            fv = None
            if self._has_field_value(fk,
                                     list(value.keys()),
                                     context.jconf_owner):
                fv = self._get_field_value(fk, value, context.jconf_owner)
            types = rtypes(ft, context.jconf_owner)
            retval[fk] = types.validator.transform(context.new(
                value=fv,
                keypath_root=concat_keypath(context.keypath_root, fk),
                keypath_owner=concat_keypath(context.keypath_owner, fk),
                keypath_parent=fk,
                parent=value,
                fdef=types.fdef))
        return retval

    def tojson(self, context: JCtx) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, dict):
            return context.value
        retval = {}
        for k, t in self.raw_shape_types(context.jconf.cls).items():
            key = camelize(k, False) if context.jconf.camelize_json_keys else k
            value_at_key = context.value.get(k)
            types = rtypes(t, context.jconf)
            if types:
                retval[key] = types.validator.tojson(context.new(value=value_at_key))
            else:
                retval[key] = value_at_key
        return retval

    def serialize(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        if not isinstance(context.value, dict):
            return context.value
        retval = {}
        for key, raw_types in self.raw_shape_types(context.jconf_owner.cls).items():
            value_at_key = context.value.get(key)
            types = rtypes(raw_types, context.jconf_owner)
            if types:
                retval[key] = types.validator.serialize(context.new(
                    value=value_at_key,
                    keypath_root=concat_keypath(context.keypath_root, key),
                    keypath_owner=concat_keypath(context.keypath_owner, key),
                    keypath_parent=key,
                    parent=context.value,
                    fdef=types.fdef))
            else:
                retval[key] = value_at_key
        return retval
