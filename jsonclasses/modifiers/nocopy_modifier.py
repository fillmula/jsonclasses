"""module for nocopy modifier."""
from ..fdef import CopyBehavior, FDef
from .modifier import Modifier


class NoCopyModifier(Modifier):
    """NoCopy modifier marks a column should be NoCopy."""

    def define(self, fdef: FDef) -> None:
        fdef._copy_behavior = CopyBehavior.NOCOPY
