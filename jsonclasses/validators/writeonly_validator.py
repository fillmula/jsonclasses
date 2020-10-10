"""module for writeonly validator."""
from ..fields import FieldDescription, ReadRule
from .validator import Validator


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.read_rule = ReadRule.NO_READ
