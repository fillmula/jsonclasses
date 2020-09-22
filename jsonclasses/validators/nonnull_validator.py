"""module for nonnull validator."""
from .validator import Validator
from ..fields import FieldDescription, Nullability
from ..contexts import ValidatingContext


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.collection_nullability = Nullability.NONNULL

    def validate(self, context: ValidatingContext) -> None:
        pass
