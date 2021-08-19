"""module for cascade validator."""
from ..fdef import Fdef, DeleteRule
from .validator import Validator


class CascadeValidator(Validator):
    """Cascade validator marks a relationship's delete rule as cascade."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.CASCADE
