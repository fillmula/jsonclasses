"""module for readwrite modifier."""
from ..fdef import Fdef, WriteRule, ReadRule
from .modifier import Modifier


class ReadwriteModifier(Modifier):
    """Readwrite modifier marks a field both readable and writable."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.UNLIMITED
        fdef._read_rule = ReadRule.UNLIMITED
