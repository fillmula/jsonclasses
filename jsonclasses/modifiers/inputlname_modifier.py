"""module for inputlname modifier."""
from ..fdef import FDef, EnumInput
from .modifier import Modifier


class InputLnameModifier(Modifier):
    """Input lname modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.LOWERCASE_NAME
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.LOWERCASE_NAME
        return
