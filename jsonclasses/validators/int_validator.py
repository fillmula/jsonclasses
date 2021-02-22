"""module for int validator."""
from ..field_definition import FieldType
from .type_validator import TypeValidator


class IntValidator(TypeValidator):
    """Int validator validates value against int type."""

    def __init__(self):
        super().__init__()
        self.cls = int
        self.field_type = FieldType.INT
        self.exact_type = True
