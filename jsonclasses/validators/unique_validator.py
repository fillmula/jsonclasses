"""module for unique validator."""
from ..fields import FieldDescription
from .validator import Validator


class UniqueValidator(Validator):
    """Unique validator marks a column should be unique."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.unique = True
