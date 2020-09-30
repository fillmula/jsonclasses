"""module for bool validator."""
from ..fields import FieldType
from .type_validator import TypeValidator


class BoolValidator(TypeValidator):
    """Bool validator validate value against bool."""

    def __init__(self):
        self.cls = bool
        self.field_type = FieldType.BOOL
