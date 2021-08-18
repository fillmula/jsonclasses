"""module for readonly validator."""
from ..field_definition import FieldDefinition, WriteRule
from .validator import Validator


class ReadonlyValidator(Validator):
    """Readonly validator marks a field to be readonly."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.write_rule = WriteRule.NO_WRITE
