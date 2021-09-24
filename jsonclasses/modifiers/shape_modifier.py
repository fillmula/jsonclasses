"""module for shape modifier."""
from __future__ import annotations
from jsonclasses.keypath import concat_keypath
from jsonclasses.vmsgcollector import VMsgCollector
from typing import Any, Sequence, Union, TYPE_CHECKING
from ..fdef import Fdef, FType, Nullability, Strictness
from ..excs import ValidationException
from ..jconf import JConf
from .type_modifier import TypeModifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class ShapeModifier(TypeModifier):
    """Shape modifier validates a dict of values with defined shape."""

    def __init__(self, raw_shape_types: Union[dict[str, Any], str]) -> None:
        super().__init__()
        self.cls = dict
        self.ftype = FType.SHAPE
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
        ctor = VMsgCollector()
        for k, types in ctx.fdef.shape_types.items():
            try:
                value_at_key = ctx.val[k]
            except KeyError:
                value_at_key = None
            try:
                ival = ctx.colval(value_at_key, k, types.fdef, ctx.val)
                types.modifier.validate(ival)
            except ValidationException as exception:
                if all_fields:
                    ctor.receive(exception.keypath_messages)
                else:
                    raise exception
        if ctor.has_msgs:
            ctx.raise_mvexc(ctor.messages)

    def _has_field_value(self,
                         field_key: str,
                         keys: Sequence[str],
                         jconf: JConf) -> bool:
        field_name = field_key
        json_field_name = jconf.key_encoding_strategy(field_name)
        return json_field_name in keys or field_name in keys

    def _get_field_value(self,
                         field_key: str,
                         value: dict[str, Any],
                         jconf: JConf) -> Any:
        field_value = value.get(field_key)
        if field_value is None:
            field_value = value.get(jconf.key_encoding_strategy(field_key))
        return field_value

    def _strictness_check(self, value: dict[str, Any], ctx: Ctx):
        value_keys = list(value.keys())
        value_keys = [ctx.jconfowner.key_decoding_strategy(k) for k in value_keys]
        keys = ctx.fdef.shape_types.keys()
        for k in value_keys:
            if k not in keys:
                kp = concat_keypath(ctx.skeypathr, k)
                ctx.raise_mvexc({kp: 'key is not allowed'})

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
            retval[fk] = types.modifier.transform(ictx)
        return retval

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if not isinstance(ctx.val, dict):
            return ctx.val
        retval = {}
        for k, types in ctx.fdef.shape_types.items():
            key = ctx.jconfowner.key_encoding_strategy(k)
            value_at_key = ctx.val.get(k)
            if types:
                retval[key] = types.modifier.tojson(ctx.nval(value_at_key))
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
                retval[key] = types.modifier.serialize(ictx)
            else:
                retval[key] = value_at_key
        return retval
