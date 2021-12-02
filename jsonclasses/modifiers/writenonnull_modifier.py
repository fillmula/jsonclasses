"""module for writenonnull modifier."""
from ..fdef import FDef, WriteRule
from .modifier import Modifier


class WriteNonnullModifier(Modifier):
    """Write nonnull modifier marks a field as writenonnull. Fields are
    allowed to be modified. However, nil value won't be set.
    """

    def define(self, fdef: FDef) -> None:
        fdef._write_rule = WriteRule.WRITE_NONNULL
