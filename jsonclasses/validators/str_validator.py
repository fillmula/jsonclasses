"""module for str validator."""
from ..field_definition import FieldType
from .type_validator import TypeValidator


class StrValidator(TypeValidator):
    """Str validator validates value against str type."""

    def __init__(self):
        super().__init__()
        self.cls = str
        self.field_type = FieldType.STR
