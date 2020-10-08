"""module for str validator."""
from ..fields import FieldType
from .type_validator import TypeValidator


class StrValidator(TypeValidator):
    """Str validator validates value against str type."""

    def __init__(self):
        super().__init__()
        self.cls = str
        self.field_type = FieldType.STR
