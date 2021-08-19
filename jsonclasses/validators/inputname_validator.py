"""module for inputname validator."""
from ..fdef import Fdef, EnumInput
from .validator import Validator


class InputNameValidator(Validator):
    """Input name validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.NAME
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.NAME
        return
