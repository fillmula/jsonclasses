"""module for linkedby modifier."""
from ..fdef import DeleteRule, Fdef, FStore
from .modifier import Modifier


class LinkedByModifier(Modifier):
    """Linked by modifier marks a field linked with a foreign key."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.FOREIGN_KEY
        fdef._foreign_key = self.foreign_key
        fdef._use_join_table = False
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
