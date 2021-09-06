"""module for linkto modifier."""
from ..fdef import DeleteRule, Fdef, FieldStorage
from .modifier import Modifier


class LinkToModifier(Modifier):
    """Link to modifier marks a field which is a local key."""

    def define(self, fdef: Fdef) -> None:
        fdef._field_storage = FieldStorage.LOCAL_KEY
        if fdef._delete_rule is None:
            fdef._delete_rule = DeleteRule.NULLIFY
