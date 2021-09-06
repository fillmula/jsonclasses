"""module for readonly modifier."""
from ..fdef import Fdef, WriteRule
from .modifier import Modifier


class ReadonlyModifier(Modifier):
    """Readonly modifier marks a field to be readonly."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.NO_WRITE
