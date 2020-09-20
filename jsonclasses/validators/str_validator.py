"""module for str validator."""
from __future__ import annotations
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class StrValidator(Validator):
    """Str validator validates value against str type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.STR

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and not isinstance(value, str):
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should be str.'},
                root
            )
