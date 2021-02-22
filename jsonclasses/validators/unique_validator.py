"""module for unique validator."""
from ..field_definition import FieldDefinition
from .validator import Validator


class UniqueValidator(Validator):
    """Unique validator marks a column should be unique."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.unique = True
