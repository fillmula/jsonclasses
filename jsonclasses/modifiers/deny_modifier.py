"""module for deny modifier."""
from ..fdef import Fdef, DeleteRule
from .modifier import Modifier


class DenyModifier(Modifier):
    """Deny modifier marks a relationship's delete rule as deny."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.DENY
