"""module for unique validator."""
from ..fdef import Fdef
from .validator import Validator


class UniqueValidator(Validator):
    """Unique validator marks a column should be unique."""

    def define(self, fdef: Fdef) -> None:
        fdef._unique = True
