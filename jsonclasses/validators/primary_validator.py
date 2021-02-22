"""module for readonly validator."""
from ..field_definitionimport FieldDefinition
from .validator import Validator


class PrimaryValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.primary = True
