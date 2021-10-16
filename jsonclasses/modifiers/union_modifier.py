"""module for union modifier."""
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..excs import ValidationException
from .modifier import Modifier
from ..rtypes import rtypes
from ..fdef import Fdef, FType
if TYPE_CHECKING:
    from ..ctx import Ctx


class UnionModifier(Modifier):
    """Union type modifier validates value against a list of available types.
    """

    def __init__(self, type_list: list[Any]) -> None:
        self.type_list = type_list

    def define(self, fdef: Fdef) -> None:
        fdef._ftype = FType.UNION
        fdef._raw_union_types = [rtypes(t) for t in self.type_list]

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        for types in ctx.fdef.raw_union_types:
            if types.fdef._cdef is None:
                types.fdef._cdef = ctx.owner.__class__.cdef
            try:
                return types.modifier.transform(ctx.alterfdef(types.fdef))
            except:
                continue
        return ctx.val

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return
        for types in ctx.fdef.raw_union_types:
            if types.fdef._cdef is None:
                types.fdef._cdef = ctx.owner.__class__.cdef
            try:
                types.modifier.validate(ctx.alterfdef(types.fdef))
                return
            except ValidationException:
                continue
        ctx.raise_vexc('value is not of any provided type')

    def serialize(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        for types in ctx.fdef.raw_union_types:
            if types.fdef._cdef is None:
                types.fdef._cdef = ctx.owner.__class__.cdef
            try:
                newctx = ctx.alterfdef(types.fdef)
                types.modifier.validate(newctx)
                return types.modifier.serialize(newctx)
            except ValidationException:
                continue
        return None

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        for types in ctx.fdef.raw_union_types:
            if types.fdef._cdef is None:
                types.fdef._cdef = ctx.owner.__class__.cdef
            try:
                newctx = ctx.alterfdef(types.fdef)
                types.modifier.validate(newctx)
                return types.modifier.tojson(newctx)
            except ValidationException:
                continue
        return None
