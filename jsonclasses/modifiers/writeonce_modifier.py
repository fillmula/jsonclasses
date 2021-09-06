"""module for writeonce modifier."""
from ..fdef import Fdef, WriteRule
from .modifier import Modifier


class WriteonceModifier(Modifier):
    """Writeonce modifier marks a field as writeonce."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.WRITE_ONCE
