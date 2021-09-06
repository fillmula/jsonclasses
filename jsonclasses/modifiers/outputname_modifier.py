"""module for outputname modifier."""
from ..fdef import Fdef, EnumOutput
from .modifier import Modifier


class OutputNameModifier(Modifier):
    """Output name modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.NAME
