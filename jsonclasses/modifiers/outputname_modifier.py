"""module for outputname modifier."""
from ..fdef import FDef, EnumOutput
from .modifier import Modifier


class OutputNameModifier(Modifier):
    """Output name modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        fdef._enum_output = EnumOutput.NAME
