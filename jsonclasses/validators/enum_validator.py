"""module for enum validator."""
from typing import Any, Union
from enum import Enum
from ..fdef import (FieldType, Fdef, EnumInput,
                                EnumOutput)
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class EnumValidator(Validator):
    """Enum validator validates value against provided enum type."""

    def __init__(self, enum_or_name: Union[type[Enum], str]):
        super().__init__()
        self.enum_or_name = enum_or_name

    def define(self, fdef: Fdef) -> None:
        fdef._field_type = FieldType.ENUM
        fdef._raw_enum_class = self.enum_or_name
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.NAME
        if fdef.enum_output is None:
            fdef._enum_output = EnumOutput.NAME
        return

    def transform(self, ctx: Ctx) -> Any:
        if ctx.value is None:
            return None
        if isinstance(self.enum_or_name, str):
            jconf = ctx.jconf_owner
            enum_class = jconf.cgraph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if isinstance(ctx.value, enum_class):
            return ctx.value
        enum_input = ctx.fdef.enum_input
        if enum_input.__contains__(EnumInput.VALUE):
            try:
                return enum_class(ctx.value)
            except ValueError:
                pass
        elif isinstance(ctx.value, str):
            if enum_input.__contains__(EnumInput.NAME):
                try:
                    return enum_class[ctx.value]
                except KeyError:
                    pass
            if enum_input.__contains__(EnumInput.LOWERCASE_NAME):
                try:
                    return enum_class[ctx.value.upper()]
                except KeyError:
                    pass

            raise ValidationException({
                ctx.keypath_root: 'unknown enum value'
            }, ctx.root)
        else:
            raise ValidationException({
                ctx.keypath_root: 'unknown enum value'
            }, ctx.root)

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return None
        if isinstance(self.enum_or_name, str):
            jconf = ctx.jconf_owner
            enum_class = jconf.cgraph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if not isinstance(ctx.value, enum_class):
            raise ValidationException({
                ctx.keypath_root: 'invalid enum value'
            }, ctx.root)

    def tojson(self, ctx: Ctx) -> Any:
        if ctx.value is None:
            return None
        if ctx.fdef.enum_output == EnumOutput.VALUE:
            return ctx.value.value
        elif ctx.fdef.enum_output == EnumOutput.NAME:
            return ctx.value.name
        elif ctx.fdef.enum_output == EnumOutput.LOWERCASE_NAME:
            return ctx.value.name.lower()
