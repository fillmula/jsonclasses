"""module for nonnull validator."""
from .validator import Validator
from ..fields import FieldDescription, Nullability


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.collection_nullability = Nullability.NONNULL
