"""module for bool validator."""
from ..field_definition import FieldType
from .type_validator import TypeValidator


class BoolValidator(TypeValidator):
    """Bool validator validate value against bool."""

    def __init__(self):
        super().__init__()
        self.cls = bool
        self.field_type = FieldType.BOOL
        self.exact_type = True
