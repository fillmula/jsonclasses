"""module for int validator."""
from typing import Any
from ..field_description import FieldDescription, FieldType
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class IntValidator(Validator):
    """Int validator validate value against int type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.INT

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and type(value) is not int:
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should be int.'},
                root
            )
