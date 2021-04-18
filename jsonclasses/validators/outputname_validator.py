"""module for outputname validator."""
from ..field_definition import FieldDefinition, EnumOutput
from .validator import Validator


class OutputNameValidator(Validator):
    """Output name validator tweaks enum validator's behavior."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.enum_output = EnumOutput.NAME
