"""module for writeonly validator."""
from ..field_definition import FieldDefinition, ReadRule
from .validator import Validator


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.read_rule = ReadRule.NO_READ
