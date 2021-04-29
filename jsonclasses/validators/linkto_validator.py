"""module for linkto validator."""
from ..field_definition import DeleteRule, FieldDefinition, FieldStorage
from .validator import Validator


class LinkToValidator(Validator):
    """Link to validator marks a field which is a local key."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.field_storage = FieldStorage.LOCAL_KEY
        if fdesc.delete_rule is None:
            fdesc.delete_rule = DeleteRule.NULLIFY
