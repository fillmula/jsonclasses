"""module for unresolved modifier."""
from ..fdef import FDef
from .modifier import Modifier


class UnresolvedModifier(Modifier):
    """This modifier contains unresolved names."""

    def __init__(self, arg: str) -> None:
        self.arg = arg

    def define(self, fdef: FDef) -> None:
        fdef._unresolved = True
        fdef._unresolved_name = self.arg
