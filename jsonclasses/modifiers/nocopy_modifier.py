"""module for nocopy modifier."""
from ..fdef import CopyBehavior, Fdef
from .modifier import Modifier


class NoCopyModifier(Modifier):
    """NoCopy modifier marks a column should be NoCopy."""

    def define(self, fdef: Fdef) -> None:
        fdef._copy_behavior = CopyBehavior.NOCOPY
