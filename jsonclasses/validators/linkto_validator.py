"""module for linkto validator."""
from ..fdef import DeleteRule, Fdef, FieldStorage
from .validator import Validator


class LinkToValidator(Validator):
    """Link to validator marks a field which is a local key."""

    def define(self, fdef: Fdef) -> None:
        fdef.field_storage = FieldStorage.LOCAL_KEY
        if fdef.delete_rule is None:
            fdef.delete_rule = DeleteRule.NULLIFY
