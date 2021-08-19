"""module for reset validator."""
from .validator import Validator
from ..fdef import Fdef


class ResetValidator(Validator):
    """A reset validator marks fields for recording value before modified.
    This is used for comparing and validating values on update.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._has_reset_validator = True
