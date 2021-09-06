"""module for eager modifier."""
from .modifier import Modifier
from ..fdef import Fdef


class EagerModifier(Modifier):
    """An EagerModifier marks fields for initialization and set stage validation.
    This is used usually before heavy transforming modifiers.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._has_eager_modifier = True
