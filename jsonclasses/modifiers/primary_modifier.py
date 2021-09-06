"""module for readonly modifier."""
from ..fdef import Fdef
from .modifier import Modifier


class PrimaryModifier(Modifier):
    """Primary modifier marks a field as the primary key."""

    def define(self, fdef: Fdef) -> None:
        fdef._primary = True
