"""module for unique modifier."""
from ..fdef import Fdef
from .modifier import Modifier


class UniqueModifier(Modifier):
    """Unique modifier marks a column should be unique."""

    def define(self, fdef: Fdef) -> None:
        fdef._unique = True
