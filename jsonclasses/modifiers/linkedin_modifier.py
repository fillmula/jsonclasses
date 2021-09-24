"""module for linkedin modifier."""
from typing import Any
from ..fdef import DeleteRule, Fdef, FStore
from .modifier import Modifier


class LinkedInModifier(Modifier):
    """Linked in modifier marks a field linked with a joinning table which is
    also a JSON Class."""

    def __init__(self, cls: Any) -> None:
        self.cls = cls

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.FOREIGN_KEY
        fdef._join_table_cls = self.cls
        fdef._use_join_table = True
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
