"""module for index modifier."""
from .modifier import Modifier
from ..fdef import Fdef


class IndexModifier(Modifier):
    """Index modifier implies this column should be indexed in database."""

    def __init__(self, unique: bool, index_name: str | None = None) -> None:
        self.unique = unique
        self.index_name = index_name

    def define(self, fdef: Fdef) -> None:
        if self.index_name:
            if self.unique:
                fdef._cunique = True
                fdef._cunique_names.append(self.index_name)
            else:
                fdef._cindex = True
                fdef._cindex_names.append(self.index_name)
        else:
            if self.unique:
                fdef._unique = True
            else:
                fdef._index = True
