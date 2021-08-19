"""module for deny validator."""
from ..fdef import Fdef, DeleteRule
from .validator import Validator


class DenyValidator(Validator):
    """Deny validator marks a relationship's delete rule as deny."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.DENY
