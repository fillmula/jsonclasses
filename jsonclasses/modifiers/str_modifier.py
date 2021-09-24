"""module for str modifier."""
from ..fdef import FType
from .type_modifier import TypeModifier


class StrModifier(TypeModifier):
    """Str modifier validates value against str type."""

    def __init__(self):
        super().__init__()
        self.cls = str
        self.ftype = FType.STR
