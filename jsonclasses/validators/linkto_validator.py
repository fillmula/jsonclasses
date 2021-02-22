"""module for linkto validator."""
from ..field_definition import FieldDefinition, FieldStorage
from .validator import Validator


class LinkToValidator(Validator):
    """Link to validator marks a field which is a local key."""

    def define(self, fdesc: FieldDefinition) -> None:
        fdesc.field_storage = FieldStorage.LOCAL_KEY
