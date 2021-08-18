"""module for readonly validator."""
from ..field_definition import FieldDefinition
from .validator import Validator


class PrimaryValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.primary = True
