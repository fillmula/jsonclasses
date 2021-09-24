"""module for bool modifier."""
from ..fdef import FType
from .type_modifier import TypeModifier


class BoolModifier(TypeModifier):
    """Bool modifier validate value against bool."""

    def __init__(self):
        super().__init__()
        self.cls = bool
        self.ftype = FType.BOOL
        self.exact_type = True
