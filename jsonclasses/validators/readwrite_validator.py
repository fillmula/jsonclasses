"""module for readwrite validator."""
from ..field_definition import FieldDefinition, WriteRule, ReadRule
from .validator import Validator


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.write_rule = WriteRule.UNLIMITED
        fdef.read_rule = ReadRule.UNLIMITED
