"""module for outputvalue validator."""
from ..fdef import Fdef, EnumOutput
from .validator import Validator


class OutputValueValidator(Validator):
    """Output value validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.VALUE
