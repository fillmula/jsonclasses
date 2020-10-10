"""module for strict validator."""
from .validator import Validator
from ..fields import FieldDescription, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.strictness = Strictness.STRICT
