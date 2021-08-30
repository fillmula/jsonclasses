"""module for shape validator."""
from __future__ import annotations
from typing import Any, Sequence, Union, TYPE_CHECKING
from inflection import underscore, camelize
from ..fdef import Fdef, FieldType, Nullability, Strictness
from ..excs import ValidationException
from ..jconf import JConf
from .type_validator import TypeValidator
if TYPE_CHECKING:
    from ..ctx import Ctx


class ShapeValidator(TypeValidator):
    """Shape validator validates a dict of values with defined shape."""

    def __init__(self, raw_shape_types: Union[dict[str, Any], str]) -> None:
        super().__init__()
        self.cls = dict
        self.field_type = FieldType.SHAPE
        self.raw_types = raw_shape_types
        self.exact_type = False

    def define(self, fdef: Fdef) -> None:
        super().define(fdef)
        fdef._raw_shape_types = self.raw_types

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        super().validate(ctx)
        all_fields = ctx.ctxcfg.all_fields
        if all_fields is None:
            all_fields = ctx.cdefowner.jconf.validate_all_fields
        keypath_messages = {}
        for k, types in ctx.fdef.shape_types.items():
            try:
                value_at_key = ctx.val[k]
            except KeyError:
                value_at_key = None
            try:
                ival = ctx.colval(value_at_key, k, types.fdef, ctx.val)
                types.validator.validate(ival)
            except ValidationException as exception:
                if all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(keypath_messages, root=ctx.root)

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

    def _strictness_check(self, value: dict[str, Any], ctx: Ctx):
        value_keys = list(value.keys())
        if ctx.jconfowner.camelize_json_keys:
            value_keys = [underscore(k) for k in value_keys]
        keys = ctx.fdef.shape_types.keys()
        for k in value_keys:
            if k not in keys:
                kp = '.'.join([str(k) for k in ctx.keypathr])
                raise ValidationException(
                    {kp: (f'Unallowed key \'{k}\' at \'{kp}\'.')}, ctx.root)

    def transform(self, ctx: Ctx) -> Any:
        value = ctx.val
        fd = ctx.fdef
        if fd.collection_nullability == Nullability.NONNULL and value is None:
            value = {}
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        if fd.strictness == Strictness.STRICT:
            self._strictness_check(value, ctx)
        retval = {}
        for fk, types in ctx.fdef.shape_types.items():
            fv = None
            if self._has_field_value(fk, list(value.keys()), ctx.jconfowner):
                fv = self._get_field_value(fk, value, ctx.jconfowner)
            ictx = ctx.colval(fv, fk, types.fdef, value)
            retval[fk] = types.validator.transform(ictx)
        return retval

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if not isinstance(ctx.val, dict):
            return ctx.val
        retval = {}
        for k, types in ctx.fdef.shape_types.items():
            key = camelize(k, False) if ctx.jconfowner.camelize_json_keys else k
            value_at_key = ctx.val.get(k)
            if types:
                retval[key] = types.validator.tojson(ctx.nval(value_at_key))
            else:
                retval[key] = value_at_key
        return retval

    def serialize(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if not isinstance(ctx.val, dict):
            return ctx.val
        retval = {}
        for key, types in ctx.fdef.shape_types.items():
            value_at_key = ctx.val.get(key)
            if types:
                ictx = ctx.colval(value_at_key, key, types.fdef, ctx.val)
                retval[key] = types.validator.serialize(ictx)
            else:
                retval[key] = value_at_key
        return retval
