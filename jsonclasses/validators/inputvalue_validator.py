"""module for inputvalue validator."""
from ..fdef import Fdef, EnumInput
from .validator import Validator


class InputValueValidator(Validator):
    """Input value validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.VALUE
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.VALUE
        return
