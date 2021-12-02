"""module for writeonce modifier."""
from ..fdef import FDef, WriteRule
from .modifier import Modifier


class WriteonceModifier(Modifier):
    """Writeonce modifier marks a field as writeonce."""

    def define(self, fdef: FDef) -> None:
        fdef._write_rule = WriteRule.WRITE_ONCE
