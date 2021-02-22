"""module for writeonce validator."""
from ..field_definition import FieldDefinition, WriteRule
from .validator import Validator


class WriteonceValidator(Validator):
    """Writeonce validator marks a field as writeonce."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.write_rule = WriteRule.WRITE_ONCE
