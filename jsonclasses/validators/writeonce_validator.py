"""module for writeonce validator."""
from ..fdef import Fdef, WriteRule
from .validator import Validator


class WriteonceValidator(Validator):
    """Writeonce validator marks a field as writeonce."""

    def define(self, fdef: Fdef) -> None:
        fdef._write_rule = WriteRule.WRITE_ONCE
