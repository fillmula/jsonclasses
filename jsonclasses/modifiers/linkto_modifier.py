"""module for linkto modifier."""
from ..fdef import DeleteRule, FType, Fdef, FStore, Nullability
from .modifier import Modifier


class LinkToModifier(Modifier):
    """Link to modifier marks a field which is a local key."""

    def define(self, fdef: Fdef) -> None:
        fdef._fstore = FStore.LOCAL_KEY
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
        if fdef._ftype == FType.LIST:
            if fdef._collection_nullability is Nullability.UNDEFINED:
                fdef._collection_nullability = Nullability.NONNULL
