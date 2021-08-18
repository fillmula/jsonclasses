"""module for inputname validator."""
from ..field_definition import FieldDefinition, EnumInput
from .validator import Validator


class InputNameValidator(Validator):
    """Input name validator tweaks enum validator's behavior."""

    def define(self, fdef: FieldDefinition) -> None:
        if fdef.enum_input is None:
            fdef.enum_input = EnumInput.NAME
        else:
            fdef.enum_input = fdef.enum_input | EnumInput.NAME
        return
