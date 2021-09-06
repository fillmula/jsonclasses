"""module for outputlname modifier."""
from ..fdef import Fdef, EnumOutput
from .modifier import Modifier


class OutputLnameModifier(Modifier):
    """Output lname modifier tweaks enum modifier's behavior."""

    def define(self, fdef: Fdef) -> None:
        fdef._enum_output = EnumOutput.LOWERCASE_NAME
