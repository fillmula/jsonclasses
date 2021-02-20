"""module for reset validator."""
from .validator import Validator
from ..fields import FieldDescription


class ResetValidator(Validator):
    """A reset validator marks fields for recording value before modified.
    This is used for comparing and validating values on update.
    """

    def define(self, fdesc: FieldDescription) -> None:
        fdesc.has_reset_validator = True
