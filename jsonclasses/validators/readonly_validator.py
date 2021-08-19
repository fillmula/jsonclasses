"""module for readonly validator."""
from ..fdef import Fdef, WriteRule
from .validator import Validator


class ReadonlyValidator(Validator):
    """Readonly validator marks a field to be readonly."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.NO_WRITE
