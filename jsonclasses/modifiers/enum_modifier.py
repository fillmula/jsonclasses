"""module for enum modifier."""
from __future__ import annotations
from typing import Any, Union, TYPE_CHECKING
from enum import Enum
from ..fdef import (FType, FDef, EnumInput,
                                EnumOutput)
from .modifier import Modifier
if TYPE_CHECKING:
    from ..ctx import Ctx


class EnumModifier(Modifier):
    """Enum modifier validates value against provided enum type."""

    def __init__(self, enum_or_name: Union[type[Enum], str]):
        super().__init__()
        self.enum_or_name = enum_or_name

    def define(self, fdef: FDef) -> None:
        fdef._ftype = FType.ENUM
        fdef._raw_enum_class = self.enum_or_name
        if fdef._enum_input is None:
            fdef._enum_input = EnumInput.NAME
        if fdef._enum_output is None:
            fdef._enum_output = EnumOutput.NAME
        return

    def transform(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if isinstance(self.enum_or_name, str):
            jconf = ctx.cdefowner.jconf
            enum_class = jconf.cgraph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if isinstance(ctx.val, enum_class):
            return ctx.val
        enum_input = ctx.fdef.enum_input
        if enum_input.__contains__(EnumInput.VALUE):
            try:
                return enum_class(ctx.val)
            except ValueError:
                pass
        elif isinstance(ctx.val, str):
            if enum_input.__contains__(EnumInput.NAME):
                try:
                    return enum_class[ctx.val]
                except KeyError:
                    pass
            if enum_input.__contains__(EnumInput.LOWERCASE_NAME):
                try:
                    return enum_class[ctx.val.upper()]
                except KeyError:
                    pass
            ctx.raise_vexc('unknown enum value')
        else:
            ctx.raise_vexc('unknown enum value')

    def validate(self, ctx: Ctx) -> None:
        if ctx.val is None:
            return None
        if isinstance(self.enum_or_name, str):
            jconf = ctx.cdefowner.jconf
            enum_class = jconf.cgraph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if not isinstance(ctx.val, enum_class):
            ctx.raise_vexc('invalid enum value')

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.val is None:
            return None
        if ctx.fdef.enum_output == EnumOutput.VALUE:
            return ctx.val.value
        elif ctx.fdef.enum_output == EnumOutput.NAME:
            return ctx.val.name
        elif ctx.fdef.enum_output == EnumOutput.LOWERCASE_NAME:
            return ctx.val.name.lower()
