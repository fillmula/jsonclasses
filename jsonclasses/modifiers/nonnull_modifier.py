"""module for nonnull modifier."""
from .modifier import Modifier
from ..fdef import FDef, Nullability


class NonnullModifier(Modifier):
    """A nonnull modifier transforms None into empty library."""

    def define(self, fdef: FDef) -> None:
        fdef._collection_nullability = Nullability.NONNULL
