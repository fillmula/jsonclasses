"""module for enum validator."""
from typing import Any, Union
from ..fdef import (FieldType, Fdef, EnumInput,
                                EnumOutput)
from ..exceptions import ValidationException
from .validator import Validator
from ..ctxs import TCtx, JCtx, VCtx


class EnumValidator(Validator):
    """Enum validator validates value against provided enum type."""

    def __init__(self, enum_or_name: Union[type, str]):
        super().__init__()
        self.enum_or_name = enum_or_name
        self.field_type = FieldType.ENUM

    def define(self, fdef: Fdef) -> None:
        fdef.field_type = FieldType.ENUM
        fdef.enum_class = self.enum_or_name
        if fdef.enum_input is None:
            fdef.enum_input = EnumInput.NAME
        if fdef.enum_output is None:
            fdef.enum_output = EnumOutput.NAME
        return

    def transform(self, context: TCtx) -> Any:
        if context.value is None:
            return None
        if isinstance(self.enum_or_name, str):
            config = context.config_owner
            enum_class = config.class_graph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if isinstance(context.value, enum_class):
            return context.value
        enum_input = context.fdef.enum_input
        if enum_input.__contains__(EnumInput.VALUE):
            try:
                return enum_class(context.value)
            except ValueError:
                pass
        elif isinstance(context.value, str):
            if enum_input.__contains__(EnumInput.NAME):
                try:
                    return enum_class[context.value]
                except KeyError:
                    pass
            if enum_input.__contains__(EnumInput.LOWERCASE_NAME):
                try:
                    return enum_class[context.value.upper()]
                except KeyError:
                    pass

            raise ValidationException({
                context.keypath_root: 'unknown enum value'
            }, context.root)
        else:
            raise ValidationException({
                context.keypath_root: 'unknown enum value'
            }, context.root)

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return None
        if isinstance(self.enum_or_name, str):
            config = context.config_owner
            enum_class = config.class_graph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if not isinstance(context.value, enum_class):
            raise ValidationException({
                context.keypath_root: 'invalid enum value'
            }, context.root)

    def tojson(self, context: JCtx) -> Any:
        if context.value is None:
            return None
        if context.fdef.enum_output == EnumOutput.VALUE:
            return context.value.value
        elif context.fdef.enum_output == EnumOutput.NAME:
            return context.value.name
        elif context.fdef.enum_output == EnumOutput.LOWERCASE_NAME:
            return context.value.name.lower()
