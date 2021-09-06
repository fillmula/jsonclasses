"""module for readonly modifier."""
from ..fdef import Fdef
from .modifier import Modifier


class UseForModifier(Modifier):
    """Primary modifier marks a field as the primary key."""

    def __init__(self, usage: str) -> None:
        self.usage = usage

    def define(self, fdef: Fdef) -> None:
        fdef._usage = self.usage
