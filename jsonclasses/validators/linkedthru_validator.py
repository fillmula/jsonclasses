"""module for linkedthru validator."""
from ..fdef import DeleteRule, Fdef, FieldStorage
from .validator import Validator


class LinkedThruValidator(Validator):
    """Linked by validator marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdef: Fdef) -> None:
        fdef._field_storage = FieldStorage.FOREIGN_KEY
        fdef._foreign_key = self.foreign_key
        fdef._use_join_table = True
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
