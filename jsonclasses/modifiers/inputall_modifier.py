"""module for inputall modifier."""
from ..fdef import FDef, EnumInput
from .modifier import Modifier


class InputAllModifier(Modifier):
    """Input all modifier tweaks enum modifier's behavior."""

    def define(self, fdef: FDef) -> None:
        fdef._enum_input = EnumInput.ALL
