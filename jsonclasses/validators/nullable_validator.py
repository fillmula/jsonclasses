"""module for nullable validator."""
from ..fdef import Fdef, Nullability
from .validator import Validator


class NullableValidator(Validator):
    """A nullable validator marks a collection item field to be nullable."""

    def define(self, fdef: Fdef) -> None:
        fdef._item_nullability = Nullability.NULLABLE
