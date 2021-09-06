"""module for reset modifier."""
from .modifier import Modifier
from ..fdef import Fdef


class ResetModifier(Modifier):
    """A reset modifier marks fields for recording value before modified.
    This is used for comparing and validating values on update.
    """

    def define(self, fdef: Fdef) -> None:
        fdef._has_reset_modifier = True
