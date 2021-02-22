"""module for nullable validator."""
from ..field_definition import FieldDefinition, Nullability
from .validator import Validator


class NullableValidator(Validator):
    """A nullable validator marks a collection item field to be nullable."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.item_nullability = Nullability.NULLABLE
