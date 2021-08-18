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
        fdef.field_storage = FieldStorage.FOREIGN_KEY
        fdef.join_table_cls = self.cls
        fdef.use_join_table = True
        if fdef.delete_rule is None:
            fdef.delete_rule = DeleteRule.NULLIFY
