"""module for nonnull validator."""
from .validator import Validator
from ..field_definition import FieldDefinition, Nullability


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.collection_nullability = Nullability.NONNULL
