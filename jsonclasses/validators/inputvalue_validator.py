"""module for inputvalue validator."""
from ..field_definition import FieldDefinition, EnumInput
from .validator import Validator


class InputValueValidator(Validator):
    """Input value validator tweaks enum validator's behavior."""

    def define(self, fdesc: FieldDefinition) -> None:
        if fdesc.enum_input is None:
            fdesc.enum_input = EnumInput.VALUE
        else:
            fdesc.enum_input = fdesc.enum_input | EnumInput.VALUE
        return
