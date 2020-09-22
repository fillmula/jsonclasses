"""module for unique validator."""
from ..fields import FieldDescription
from .validator import Validator
from ..contexts import ValidatingContext


class UniqueValidator(Validator):
    """Unique validator marks a column should be unique."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.unique = True

    def validate(self, context: ValidatingContext) -> None:
        pass
