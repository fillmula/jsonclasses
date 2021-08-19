"""module for readonly validator."""
from ..fdef import Fdef
from .validator import Validator


class PrimaryValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def define(self, fdef: Fdef) -> None:
        fdef._primary = True
