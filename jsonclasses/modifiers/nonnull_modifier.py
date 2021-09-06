"""module for nonnull modifier."""
from .modifier import Modifier
from ..fdef import Fdef, Nullability


class NonnullModifier(Modifier):
    """A nonnull modifier transforms None into empty library."""

    def define(self, fdef: Fdef) -> None:
        fdef._collection_nullability = Nullability.NONNULL
