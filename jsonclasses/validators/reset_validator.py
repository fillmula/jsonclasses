"""module for reset validator."""
from .validator import Validator
from ..field_definition import FieldDefinition


class ResetValidator(Validator):
    """A reset validator marks fields for recording value before modified.
    This is used for comparing and validating values on update.
    """

    def define(self, fdef: FieldDefinition) -> None:
        fdef.has_reset_validator = True
