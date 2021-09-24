"""module for int modifier."""
from ..fdef import FType
from .type_modifier import TypeModifier


class IntModifier(TypeModifier):
    """Int modifier validates value against int type."""

    def __init__(self):
        super().__init__()
        self.cls = int
        self.ftype = FType.INT
        self.exact_type = True
