"""module for writeonly validator."""
from ..fields import FieldDescription, ReadRule
from .validator import Validator
from ..contexts import ValidatingContext


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.read_rule = ReadRule.NO_READ

    def validate(self, context: ValidatingContext) -> None:
        pass
