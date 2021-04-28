"""module for enum validator."""
from typing import Any, Union
from ..field_definition import (FieldType, FieldDefinition, EnumInput,
                                EnumOutput)
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import TransformingContext, ToJSONContext, ValidatingContext


class EnumValidator(Validator):
    """Enum validator validates value against provided enum type."""

    def __init__(self, enum_or_name: Union[type, str]):
        super().__init__()
        self.enum_or_name = enum_or_name
        self.field_type = FieldType.ENUM

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.field_type = FieldType.ENUM
        fdesc.enum_class = self.enum_or_name
        if fdesc.enum_input is None:
            fdesc.enum_input = EnumInput.NAME
        if fdesc.enum_output is None:
            fdesc.enum_output = EnumOutput.NAME
        return

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        if isinstance(self.enum_or_name, str):
            config = context.config_owner
            enum_class = config.class_graph.fetch_enum(self.enum_or_name)
        else:
            enum_class = self.enum_or_name
        if isinstance(context.value, enum_class):
            return context.value
        enum_input = context.definition.enum_input
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

    def validate(self, context: ValidatingContext) -> None:
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

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is None:
            return None
        if context.definition.enum_output == EnumOutput.VALUE:
            return context.value.value
        elif context.definition.enum_output == EnumOutput.NAME:
            return context.value.name
        elif context.definition.enum_output == EnumOutput.LOWERCASE_NAME:
            return context.value.name.lower()
