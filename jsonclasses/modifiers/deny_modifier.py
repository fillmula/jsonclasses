"""module for deny modifier."""
from ..fdef import FDef, DeleteRule
from .modifier import Modifier


class DenyModifier(Modifier):
    """Deny modifier marks a relationship's delete rule as deny."""

    def define(self, fdef: FDef) -> None:
        fdef._delete_rule = DeleteRule.DENY
