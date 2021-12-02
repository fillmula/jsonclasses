"""module for readonly modifier."""
from ..fdef import FDef
from .modifier import Modifier


class PrimaryModifier(Modifier):
    """Primary modifier marks a field as the primary key."""

    def define(self, fdef: FDef) -> None:
        fdef._primary = True
