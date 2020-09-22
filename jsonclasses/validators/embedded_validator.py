"""module for embedded validator."""
from ..fields import FieldDescription, FieldStorage
from .validator import Validator
from ..contexts import ValidatingContext


class EmbeddedValidator(Validator):
    """This validator marks value as embedded on the hosting object."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.EMBEDDED

    def validate(self, context: ValidatingContext) -> None:
        pass
