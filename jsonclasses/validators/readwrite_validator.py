"""module for readwrite validator."""
from ..fdef import Fdef, WriteRule, ReadRule
from .validator import Validator


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.UNLIMITED
        fdef._read_rule = ReadRule.UNLIMITED
