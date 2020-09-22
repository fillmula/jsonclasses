"""module for nullable validator."""
from ..fields import FieldDescription, Nullability
from .validator import Validator
from ..contexts import ValidatingContext


class NullableValidator(Validator):
    """A nullable validator marks a collection item field to be nullable."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.item_nullability = Nullability.NULLABLE

    def validate(self, context: ValidatingContext) -> None:
        pass
