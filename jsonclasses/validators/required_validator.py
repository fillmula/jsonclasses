"""module for required validator."""
from typing import Any
from ..field_description import FieldDescription
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class RequiredValidator(Validator):
    """Mark a field as required."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.required = True

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is None:
            raise ValidationException(
                {key_path: f'Value at \'{key_path}\' should not be None.'},
                root
            )
