"""module for writeonly validator."""
from ..field_definitionimport FieldDefinition, ReadRule
from .validator import Validator


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.read_rule = ReadRule.NO_READ
