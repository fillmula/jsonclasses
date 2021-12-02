"""module for temp modifier."""
from .modifier import Modifier
from ..fdef import FStore, FDef


class TempModifier(Modifier):
    """A temp modifier marks a field as temporary field. Value of temporary
    field is never written to database. As long as database write happens,
    temporary fields' values are set to None.
    """

    def define(self, fdef: FDef) -> None:
        fdef._fstore = FStore.TEMP
