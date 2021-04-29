"""module for linkedthru validator."""
from ..field_definition import DeleteRule, FieldDefinition, FieldStorage
from .validator import Validator


class LinkedThruValidator(Validator):
    """Linked by validator marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.field_storage = FieldStorage.FOREIGN_KEY
        fdesc.foreign_key = self.foreign_key
        fdesc.use_join_table = True
        if fdesc.delete_rule is None:
            fdesc.delete_rule = DeleteRule.NULLIFY
