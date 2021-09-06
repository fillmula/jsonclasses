"""module for cascade modifier."""
from ..fdef import Fdef, DeleteRule
from .modifier import Modifier


class CascadeModifier(Modifier):
    """Cascade modifier marks a relationship's delete rule as cascade."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.CASCADE
