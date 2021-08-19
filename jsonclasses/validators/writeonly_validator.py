"""module for writeonly validator."""
from ..fdef import Fdef, ReadRule
from .validator import Validator


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, fdef: Fdef) -> None:
        fdef._read_rule = ReadRule.NO_READ
