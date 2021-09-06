"""module for bool modifier."""
from ..fdef import FieldType
from .type_modifier import TypeModifier


class BoolModifier(TypeModifier):
    """Bool modifier validate value against bool."""

    def __init__(self):
        super().__init__()
        self.cls = bool
        self.field_type = FieldType.BOOL
        self.exact_type = True
