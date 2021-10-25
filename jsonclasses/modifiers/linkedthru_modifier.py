"""module for linkedthru modifier."""
from ..fdef import DeleteRule, Fdef, FStore, FType, Nullability
from .modifier import Modifier


class LinkedThruModifier(Modifier):
    """Linked by modifier marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.FOREIGN_KEY
        fdef._foreign_key = self.foreign_key
        fdef._use_join_table = True
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
        if fdef._ftype == FType.LIST:
            if fdef._collection_nullability is Nullability.UNDEFINED:
                fdef._collection_nullability = Nullability.NONNULL
