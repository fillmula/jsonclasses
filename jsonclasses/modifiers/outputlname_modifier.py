"""module for outputlname modifier."""
from ..fdef import FDef, EnumOutput
from .modifier import Modifier


class OutputLnameModifier(Modifier):
    """Output lname modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        fdef._enum_output = EnumOutput.LOWERCASE_NAME
