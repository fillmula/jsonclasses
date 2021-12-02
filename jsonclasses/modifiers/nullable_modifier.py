"""module for nullable modifier."""
from ..fdef import FDef, Nullability
from .modifier import Modifier


class NullableModifier(Modifier):
    """A nullable modifier marks a collection item field to be nullable."""

    def define(self, fdef: FDef) -> None:
        fdef._item_nullability = Nullability.NULLABLE
