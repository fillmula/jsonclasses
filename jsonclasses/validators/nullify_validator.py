"""module for nullify validator."""
from ..fdef import Fdef, DeleteRule
from .validator import Validator


class NullifyValidator(Validator):
    """Nullify validator marks a relationship's delete rule as nullify."""

    def define(self, fdef: Fdef) -> None:
        fdef._delete_rule = DeleteRule.NULLIFY
