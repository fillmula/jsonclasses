"""module for embedded validator."""
from ..field_definition import FieldDefinition, FieldStorage
from .validator import Validator


class EmbeddedValidator(Validator):
    """This validator marks value as embedded on the hosting object."""

    def define(self, fdef: FieldDefinition) -> None:
        fdef.field_storage = FieldStorage.EMBEDDED
