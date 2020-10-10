"""module for readwrite validator."""
from ..fields import FieldDescription, WriteRule, ReadRule
from .validator import Validator


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.write_rule = WriteRule.UNLIMITED
        fdesc.read_rule = ReadRule.UNLIMITED
