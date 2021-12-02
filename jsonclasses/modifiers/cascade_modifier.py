"""module for cascade modifier."""
from ..fdef import FDef, DeleteRule
from .modifier import Modifier


class CascadeModifier(Modifier):
    """Cascade modifier marks a relationship's delete rule as cascade."""

    def define(self, fdef: FDef) -> None:
        fdef._delete_rule = DeleteRule.CASCADE
