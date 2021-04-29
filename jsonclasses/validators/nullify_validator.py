"""module for nullify validator."""
from ..field_definition import FieldDefinition, DeleteRule
from .validator import Validator


class NullifyValidator(Validator):
    """Nullify validator marks a relationship's delete rule as nullify."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.delete_rule = DeleteRule.NULLIFY
