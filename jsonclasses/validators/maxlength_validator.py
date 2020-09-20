"""module for maxlength validator."""
from typing import Any
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class MaxlengthValidator(Validator):
    """Match validator validates value against max length."""

    def __init__(self, maxlength: int) -> None:
        self.maxlength = maxlength

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and len(value) > self.maxlength:
            raise ValidationException(
                {key_path: f'Length of value \'{value}\' at \'{key_path}\' should not be greater than {self.maxlength}.'},
                root
            )
