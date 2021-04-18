"""module for outputlname validator."""
from ..field_definition import FieldDefinition, EnumOutput
from .validator import Validator


class OutputLnameValidator(Validator):
    """Output lname validator tweaks enum validator's behavior."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.enum_output = EnumOutput.LOWERCASE_NAME
