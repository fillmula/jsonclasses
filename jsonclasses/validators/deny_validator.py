"""module for deny validator."""
from ..field_definition import FieldDefinition, DeleteRule
from .validator import Validator


class DenyValidator(Validator):
    """Deny validator marks a relationship's delete rule as deny."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.delete_rule = DeleteRule.DENY
