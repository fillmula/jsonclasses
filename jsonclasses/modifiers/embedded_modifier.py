"""module for embedded modifier."""
from ..fdef import Fdef, FieldStorage
from .modifier import Modifier


class EmbeddedModifier(Modifier):
    """This modifier marks value as embedded on the hosting object."""

    def define(self, fdef: Fdef) -> None:
        fdef._field_storage = FieldStorage.EMBEDDED
