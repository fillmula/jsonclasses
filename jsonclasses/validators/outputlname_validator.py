"""module for outputlname validator."""
from ..fdef import Fdef, EnumOutput
from .validator import Validator


class OutputLnameValidator(Validator):
    """Output lname validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.LOWERCASE_NAME
