"""module for writeonce validator."""
from ..fields import FieldDescription, WriteRule
from .validator import Validator
from ..contexts import ValidatingContext


class WriteonceValidator(Validator):
    """Writeonce validator marks a field as writeonce."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.WRITE_ONCE

    def validate(self, context: ValidatingContext) -> None:
        pass
