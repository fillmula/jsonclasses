"""module for index modifier."""
from .modifier import Modifier
from ..fdef import Fdef


class IndexModifier(Modifier):
    """Index modifier implies this column should be indexed in database."""

    def define(self, fdef: Fdef) -> None:
        fdef._index = True
