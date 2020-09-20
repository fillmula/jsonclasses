"""module for float validator."""
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class FloatValidator(Validator):
    """Date validator validate value against float type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.FLOAT

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and type(value) is not float:
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should be float.'},
                root
            )

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        if value is None:
            return None
        elif type(value) is int:
            return float(value)
        else:
            return value
