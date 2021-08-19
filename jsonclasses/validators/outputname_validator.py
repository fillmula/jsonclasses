"""module for outputname validator."""
from ..fdef import Fdef, EnumOutput
from .validator import Validator


class OutputNameValidator(Validator):
    """Output name validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.NAME
