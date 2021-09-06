"""module for nullable modifier."""
from ..fdef import Fdef, Nullability
from .modifier import Modifier


class NullableModifier(Modifier):
    """A nullable modifier marks a collection item field to be nullable."""

    def define(self, fdef: Fdef) -> None:
        fdef._item_nullability = Nullability.NULLABLE
