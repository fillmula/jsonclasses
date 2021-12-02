"""module for preserialize modifier."""
from .modifier import Modifier
from ..fdef import FDef


class PreserializeModifier(Modifier):
    """A PreserializeModifier tweaks field validation logic. Every modifier
    after a preserialize modifier are only triggered just before serialization
    into database.

    This is usually used before setonsave modifier.
    """

    def define(self, fdef: FDef) -> None:
        fdef._has_preserialize_modifier = True
