"""module for inputname modifier."""
from ..fdef import Fdef, EnumInput
from .modifier import Modifier


class InputNameModifier(Modifier):
    """Input name modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        if fdef.enum_input is None:
            fdef._enum_input = EnumInput.NAME
        else:
            fdef._enum_input = fdef.enum_input | EnumInput.NAME
        return
