"""module for strict validator."""
from .validator import Validator
from ..fdef import Fdef, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, fdef: Fdef) -> None:
        fdef._strictness = Strictness.STRICT
