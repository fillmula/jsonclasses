"""module for instanceof validator."""
from __future__ import annotations
from jsonclasses.jfield import JField
from typing import Any, Sequence, Union, cast, TYPE_CHECKING
from inflection import camelize
from ..fdef import (
    Fdef, FieldStorage, FieldType, Nullability, WriteRule, ReadRule, Strictness
)
from ..excs import ValidationException
from .validator import Validator
from ..keypath import concat_keypath, initial_keypaths
if TYPE_CHECKING:
    from ..jobject import JObject
    from ..ctx import Ctx


class InstanceOfValidator(Validator):
    """InstanceOf validator validates and transforms JSON Class instance."""

    def __init__(self, raw_type: Union[str, type[JObject]]) -> None:
        self.raw_type = raw_type

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.INSTANCE
        fdef._raw_inst_types = self.raw_type

    def validate(self, ctx: Ctx) -> None:
        from ..jobject import JObject
        # only validate if there is a value
        if ctx.val is None:
            return
        # only validate an instance once in the circular referenced map
        if ctx.mgraph.has(ctx.val):
            return
        ctx.mgraph.put(ctx.val)
        cls = cast(type[JObject], ctx.fdef.inst_cls)
        all_fields = ctx.ctxcfg.all_fields
        if all_fields is None:
            all_fields = cls.cdef.jconf.validate_all_fields
        if not isinstance(ctx.val, cls):
            raise ValidationException({
                '.'.join([str(k) for k in ctx.keypathr]): (f"Value at '{'.'.join([str(k) for k in ctx.keypathr])}' "
                                   f"should be instance of "
                                   f"'{cls.__name__}'.")
            }, ctx.root)
        only_validate_modified = not ctx.val.is_new
        modified_fields = []
        if only_validate_modified:
            modified_fields = list(initial_keypaths((ctx.val.modified_fields)))
        keypath_messages = {}
        val = cast(JObject, ctx.val)
        for field in val.__class__.cdef.fields:
            fname = field.name
            ffdef = field.fdef
            fval = getattr(ctx.val, fname)
            if field.fdef.field_storage == FieldStorage.EMBEDDED:
                if only_validate_modified and fname not in modified_fields:
                    continue
            try:
                if field.fdef.field_type == FieldType.INSTANCE:
                    fval_ctx = ctx.nexto(fval, fname, ffdef)
                else:
                    fval_ctx = ctx.nextvo(fval, fname, ffdef, ctx.original or val)
                field.types.validator.validate(fval_ctx)
            except ValidationException as exception:
                if all_fields:
                    keypath_messages.update(exception.keypath_messages)
                else:
                    raise exception
        if len(keypath_messages) > 0:
            raise ValidationException(
                keypath_messages=keypath_messages,
                root=ctx.root)

    def _strictness_check(self, ctx: Ctx, dest: JObject) -> None:
        available_names = dest.__class__.cdef.available_names
        for k in ctx.val.keys():
            if k not in available_names:
                kp = concat_keypath('.'.join([str(k) for k in ctx.keypathr]), k)
                if '.'.join([str(k) for k in ctx.keypathr]) == '':
                    msg = f'Key \'{k}\' is not allowed.'
                else:
                    kpnok = concat_keypath('.'.join([str(k) for k in ctx.keypathr]))
                    msg = f'Key \'{k}\' at \'{kpnok}\' is not allowed.'
                raise ValidationException({kp: msg}, ctx.root)

    def _fill_default_value(self, field: JField, dest: JObject, ctx: Ctx):
        if field.default is not None:
            setattr(dest, field.name, field.default)
        else:
            dctx = ctx.default(ctx.original, field.name, field.fdef)
            tsfmd = field.types.validator.transform(dctx)
            setattr(dest, field.name, tsfmd)

    def _has_field_value(self, field: JField, keys: Sequence[str]) -> bool:
        return field.json_name in keys or field.name in keys

    def _get_field_value(self, field: JField, ctx: Ctx) -> Any:
        field_value = ctx.val.get(field.json_name)
        if field_value is None and ctx.cdefowner.jconf.camelize_json_keys:
            field_value = ctx.val.get(field.name)
        return field_value

    # pylint: disable=arguments-differ, too-many-locals, too-many-branches
    def transform(self, ctx: Ctx) -> Any:
        from ..types import Types
        from ..jobject import JObject
        # handle non normal value
        if ctx.val is None:
            return ctx.original
        if not isinstance(ctx.val, dict):
            return ctx.original if ctx.original is not None else ctx.val
        # figure out types, cls and dest
        cls = cast(type[JObject], ctx.fdef.inst_cls)
        pfield = cls.cdef.primary_field
        if pfield:
            pkey = pfield.name
            pvalue = cast(Union[str, int, None], ctx.val.get(pkey))
        else:
            pvalue = None
        soft_apply_mode = False
        if ctx.original is not None:
            dest = ctx.original
            if pvalue is not None:
                ctx.mgraph.putp(pvalue, dest)
        elif pvalue is not None:
            exist_item = ctx.mgraph.getp(cls, pvalue)
            if exist_item is not None:
                dest = exist_item
                soft_apply_mode = True
            else:
                dest = cls()
                ctx.mgraph.putp(pvalue, dest)
        else:
            dest = cls()
            ctx.mgraph.put(dest)

        # strictness check
        strictness = cast(bool, cls.cdef.jconf.strict_input)
        if ctx.fdef is not None:
            if ctx.fdef.strictness == Strictness.STRICT:
                strictness = True
            elif ctx.fdef.strictness == Strictness.UNSTRICT:
                strictness = False
        if strictness:
            self._strictness_check(ctx, dest)
        # fill values
        dict_keys = list(ctx.val.keys())
        nonnull_ref_lists: list[str] = []
        for field in dest.__class__.cdef.fields:
            if not self._has_field_value(field, dict_keys):
                if field.fdef.is_ref:
                    fdef = field.fdef
                    if fdef.field_type == FieldType.LIST:
                        if fdef.collection_nullability == Nullability.NONNULL:
                            nonnull_ref_lists.append(field.name)
                    elif fdef.field_storage == FieldStorage.LOCAL_KEY:
                        tsfm = dest.__class__.cdef.jconf.key_transformer
                        refname = tsfm(field)
                        if ctx.val.get(refname) is not None:
                            setattr(dest, refname, ctx.val.get(refname))
                        crefname = camelize(refname, False)
                        if ctx.val.get(crefname) is not None:
                            setattr(dest, refname, ctx.val.get(crefname))
                    pass
                elif ctx.ctxcfg.fill_dest_blanks and not soft_apply_mode:
                    self._fill_default_value(field, dest, ctx)
                continue
            field_value = self._get_field_value(field, ctx)
            allow_write_field = True
            if field.fdef.write_rule == WriteRule.NO_WRITE:
                allow_write_field = False
            if field.fdef.write_rule == WriteRule.WRITE_ONCE:
                cfv = getattr(dest, field.name)
                if (cfv is not None) and (not isinstance(cfv, Types)):
                    allow_write_field = False
            if field.fdef.write_rule == WriteRule.WRITE_NONNULL:
                if field_value is None:
                    allow_write_field = False
            if not allow_write_field:
                if ctx.ctxcfg.fill_dest_blanks:
                    self._fill_default_value(field, dest, ctx)
                continue
            fctx = ctx.nextvo(field_value, field.name, field.fdef, dest)
            tsfmd = field.types.validator.transform(fctx)
            setattr(dest, field.name, tsfmd)
        for cname in nonnull_ref_lists:
            if getattr(dest, cname) is None:
                setattr(dest, cname, [])
        return dest

    def tojson(self, ctx: Ctx) -> Any:
        from ..jobject import JObject
        if ctx.val is None:
            return None
        val = cast(JObject, ctx.val)
        retval = {}
        clschain = ctx.idchain
        cls_name = val.__class__.cdef.name
        no_key_refs = cls_name in clschain
        for field in val.__class__.cdef.fields:
            fval = getattr(val, field.name)
            fd = field.types.fdef
            jf_name = field.json_name
            ignore_writeonly = ctx.ctxcfg.ignore_writeonly
            if fd.field_storage == FieldStorage.LOCAL_KEY and no_key_refs:
                continue
            if fd.field_storage == FieldStorage.FOREIGN_KEY and no_key_refs:
                continue
            if fd.read_rule == ReadRule.NO_READ and not ignore_writeonly:
                continue
            if fd.is_temp_field:
                continue
            if field.fdef.field_type == FieldType.INSTANCE:
                ictx = ctx.nextoc(fval, field.name, field.fdef, cls_name)
            else:
                ictx = ctx.nextvc(fval, field.name, field.fdef, cls_name)
            retval[jf_name] = field.types.validator.tojson(ictx)
        return retval

    def serialize(self, ctx: Ctx) -> Any:
        from ..jobject import JObject
        value = cast(JObject, ctx.val)
        if value is None:
            return None
        exist_item = ctx.mgraph.get(value)
        if exist_item is not None:  # Don't do twice for an object
            return value
        ctx.mgraph.put(value)
        should_update = False
        if value.is_modified or value.is_new:
            should_update = True
        for field in value.__class__.cdef.fields:
            if field.fdef.is_ref or field.fdef.is_inst or should_update:
                if field.fdef.field_storage == FieldStorage.LOCAL_KEY:
                    if getattr(value, field.name) is None:
                        tsf = value.__class__.cdef.jconf.key_transformer
                        if getattr(value, tsf(field)) is not None:
                            continue
                field_value = getattr(value, field.name)
                fctx = ctx.nextv(field_value, field.name, field.fdef)
                tsfmd = field.types.validator.serialize(fctx)
                setattr(value, field.name, tsfmd)
        return value
