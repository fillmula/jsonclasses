"""module for writeonly modifier."""
from ..fdef import FDef, ReadRule
from .modifier import Modifier


class WriteonlyModifier(Modifier):
    """Writeonly modifier marks a field as writeonly."""

    def define(self, fdef: FDef) -> None:
        fdef._read_rule = ReadRule.NO_READ
