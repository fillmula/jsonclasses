"""module for nonnull validator."""
from .validator import Validator
from ..fdef import Fdef, Nullability


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def define(self, fdef: Fdef) -> None:
        fdef.collection_nullability = Nullability.NONNULL
