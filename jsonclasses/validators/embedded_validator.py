"""module for embedded validator."""
from ..fdef import Fdef, FieldStorage
from .validator import Validator


class EmbeddedValidator(Validator):
    """This validator marks value as embedded on the hosting object."""

    def define(self, fdef: Fdef) -> None:
        fdef._field_storage = FieldStorage.EMBEDDED
