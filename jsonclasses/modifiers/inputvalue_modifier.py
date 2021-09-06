"""module for inputvalue modifier."""
from ..fdef import Fdef, EnumInput
from .modifier import Modifier


class InputValueModifier(Modifier):
    """Input value modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.VALUE
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.VALUE
        return
