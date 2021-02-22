"""module for readwrite validator."""
from ..field_definition import FieldDefinition, WriteRule, ReadRule
from .validator import Validator


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.write_rule = WriteRule.UNLIMITED
        fdesc.read_rule = ReadRule.UNLIMITED
