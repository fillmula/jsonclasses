"""module for inputlname modifier."""
from ..fdef import Fdef, EnumInput
from .modifier import Modifier


class InputLnameModifier(Modifier):
    """Input lname modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.LOWERCASE_NAME
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.LOWERCASE_NAME
        return
