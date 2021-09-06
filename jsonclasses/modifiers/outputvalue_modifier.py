"""module for outputvalue modifier."""
from ..fdef import Fdef, EnumOutput
from .modifier import Modifier


class OutputValueModifier(Modifier):
    """Output value modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.VALUE
