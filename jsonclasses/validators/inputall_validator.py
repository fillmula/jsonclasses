"""module for inputall validator."""
from ..field_definition import FieldDefinition, EnumInput
from .validator import Validator


class InputAllValidator(Validator):
    """Input all validator tweaks enum validator's behavior."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.enum_input = EnumInput.ALL
