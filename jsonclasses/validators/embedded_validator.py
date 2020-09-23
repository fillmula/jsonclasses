"""module for embedded validator."""
from ..fields import FieldDescription, FieldStorage
from .validator import Validator


class EmbeddedValidator(Validator):
    """This validator marks value as embedded on the hosting object."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.EMBEDDED
