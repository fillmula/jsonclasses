"""module for nullify modifier."""
from ..fdef import FDef, DeleteRule
from .modifier import Modifier


class NullifyModifier(Modifier):
    """Nullify modifier marks a relationship's delete rule as nullify."""

    def define(self, fdef: FDef) -> None:
        fdef._delete_rule = DeleteRule.NULLIFY
