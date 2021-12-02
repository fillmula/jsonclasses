"""module for outputvalue modifier."""
from ..fdef import FDef, EnumOutput
from .modifier import Modifier


class OutputValueModifier(Modifier):
    """Output value modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        fdef._enum_output = EnumOutput.VALUE
