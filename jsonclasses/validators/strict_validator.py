"""module for strict validator."""
from .validator import Validator
from ..fields import FieldDescription, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.strictness = Strictness.STRICT
