"""module for inputlname validator."""
from ..field_definition import FieldDefinition, EnumInput
from .validator import Validator


class InputLnameValidator(Validator):
    """Input lname validator tweaks enum validator's behavior."""

    def define(self, fdesc: FieldDefinition) -> None:
        if fdesc.enum_input is None:
            fdesc.enum_input = EnumInput.LOWERCASE_NAME
        else:
            fdesc.enum_input = fdesc.enum_input | EnumInput.LOWERCASE_NAME
        return
