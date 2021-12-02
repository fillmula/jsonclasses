"""module for inputvalue modifier."""
from ..fdef import FDef, EnumInput
from .modifier import Modifier


class InputValueModifier(Modifier):
    """Input value modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.VALUE
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.VALUE
        return
