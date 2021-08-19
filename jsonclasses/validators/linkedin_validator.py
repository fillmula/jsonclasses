"""module for linkedin validator."""
from typing import Any
from ..fdef import DeleteRule, Fdef, FieldStorage
from .validator import Validator


class LinkedInValidator(Validator):
    """Linked in validator marks a field linked with a joinning table which is
    also a JSON Class."""

    def __init__(self, cls: Any) -> None:
        self.cls = cls

    def define(self, fdef: Fdef) -> None:
        fdef._field_storage = FieldStorage.FOREIGN_KEY
        fdef._join_table_cls = self.cls
        fdef._use_join_table = True
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
