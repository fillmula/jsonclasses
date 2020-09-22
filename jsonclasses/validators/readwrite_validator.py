"""module for readwrite validator."""
from ..fields import FieldDescription, WriteRule, ReadRule
from .validator import Validator
from ..contexts import ValidatingContext


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.UNLIMITED
        field_description.read_rule = ReadRule.UNLIMITED

    def validate(self, context: ValidatingContext) -> None:
        pass
