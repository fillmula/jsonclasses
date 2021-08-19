"""module for inputall validator."""
from ..fdef import Fdef, EnumInput
from .validator import Validator


class InputAllValidator(Validator):
    """Input all validator tweaks enum validator's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_input = EnumInput.ALL
