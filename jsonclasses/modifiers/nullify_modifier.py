"""module for nullify modifier."""
from ..fdef import Fdef, DeleteRule
from .modifier import Modifier


class NullifyModifier(Modifier):
    """Nullify modifier marks a relationship's delete rule as nullify."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.NULLIFY
