"""module for queryable modifier."""
from ..fdef import Fdef, Queryability
from .modifier import Modifier


class QueryableModifier(Modifier):
    """Queryable modifier marks a column should be queryable."""

    def define(self, fdef: Fdef) -> None:
        fdef._queryability = Queryability.QUERYABLE
