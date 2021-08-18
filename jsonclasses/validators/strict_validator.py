"""module for strict validator."""
from .validator import Validator
from ..field_definition import FieldDefinition, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.strictness = Strictness.STRICT
