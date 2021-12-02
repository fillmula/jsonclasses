"""module for queryable modifier."""
from ..fdef import FDef, Queryability
from .modifier import Modifier


class QueryableModifier(Modifier):
    """Queryable modifier marks a column should be queryable."""

    def define(self, fdef: FDef) -> None:
        fdef._queryability = Queryability.QUERYABLE
