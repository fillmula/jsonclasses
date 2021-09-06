"""module for strict modifier."""
from .modifier import Modifier
from ..fdef import Fdef, Strictness


class StrictModifier(Modifier):
    """A strict modifier marks shape to disallow undefined keys."""

    def define(self, fdef: Fdef) -> None:
        fdef._strictness = Strictness.STRICT
