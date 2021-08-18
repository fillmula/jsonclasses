"""module for linkedby validator."""
from ..field_definition import DeleteRule, FieldDefinition, FieldStorage
from .validator import Validator


class LinkedByValidator(Validator):
    """Linked by validator marks a field linked with a foreign key."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdef: FieldDefinition) -> None:
        fdef.field_storage = FieldStorage.FOREIGN_KEY
        fdef.foreign_key = self.foreign_key
        fdef.use_join_table = False
        if fdef.delete_rule is None:
            fdef.delete_rule = DeleteRule.NULLIFY
