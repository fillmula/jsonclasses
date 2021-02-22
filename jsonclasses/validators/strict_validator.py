"""module for strict validator."""
from .validator import Validator
from ..field_definition import FieldDefinition, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.strictness = Strictness.STRICT
