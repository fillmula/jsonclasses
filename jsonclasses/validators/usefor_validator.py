"""module for readonly validator."""
from ..field_definition import FieldDefinition
from .validator import Validator


class UseForValidator(Validator):
    """Primary validator marks a field as the primary key."""

    def __init__(self, usage: str) -> None:
        self.usage = usage

    def define(self, fdef: FieldDefinition) -> None:
        fdef.usage = self.usage
