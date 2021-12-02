"""module for unqueryable modifier."""
from ..fdef import FDef, Queryability
from .modifier import Modifier


class UnqueryableModifier(Modifier):
    """Unqueryable modifier marks a column should be unqueryable."""

    def define(self, fdef: FDef) -> None:
        fdef._queryability = Queryability.UNQUERYABLE
