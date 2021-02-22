"""module for strict validator."""
from .validator import Validator
from ..field_definitionimport FieldDefinition, Strictness


class StrictValidator(Validator):
    """A strict validator marks shape to disallow undefined keys."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.strictness = Strictness.STRICT
