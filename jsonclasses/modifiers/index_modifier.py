"""module for index modifier."""
from .modifier import Modifier
from ..fdef import Fdef


class IndexModifier(Modifier):
    """Index modifier implies this column should be indexed in database."""

    def __init__(self, index_name: str | None = None) -> None:
        self.index_name = index_name

    def define(self, fdef: Fdef) -> None:
        if self.index_name:
            fdef._cindex = True
            fdef._cindex_names.append(self.index_name)
        else:
            fdef._index = True
