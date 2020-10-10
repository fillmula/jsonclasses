"""module for readonly validator."""
from ..fields import FieldDescription, WriteRule
from .validator import Validator


class ReadonlyValidator(Validator):
    """Readonly validator marks a field to be readonly."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.write_rule = WriteRule.NO_WRITE
