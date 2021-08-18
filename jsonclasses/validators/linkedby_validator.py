"""module for linkedby validator."""
from ..fdef import DeleteRule, Fdef, FieldStorage
from .validator import Validator


class LinkedByValidator(Validator):
    """Linked by validator marks a field linked with a foreign key."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdef: Fdef) -> None:
        fdef.field_storage = FieldStorage.FOREIGN_KEY
        fdef.foreign_key = self.foreign_key
        fdef.use_join_table = False
        if fdef.delete_rule is None:
            fdef.delete_rule = DeleteRule.NULLIFY
