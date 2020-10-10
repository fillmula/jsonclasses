"""module for nullable validator."""
from ..fields import FieldDescription, Nullability
from .validator import Validator


class NullableValidator(Validator):
    """A nullable validator marks a collection item field to be nullable."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.item_nullability = Nullability.NULLABLE
