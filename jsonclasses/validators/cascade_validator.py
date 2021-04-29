"""module for cascade validator."""
from ..field_definition import FieldDefinition, DeleteRule
from .validator import Validator


class CascadeValidator(Validator):
    """Cascade validator marks a relationship's delete rule as cascade."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.delete_rule = DeleteRule.CASCADE
