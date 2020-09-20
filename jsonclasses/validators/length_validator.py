"""module for length validator."""
from typing import Any, Optional
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class LengthValidator(Validator):
    """Length validator validate value against the provided length."""

    def __init__(self, minlength: int, maxlength: Optional[int]) -> None:
        self.minlength = minlength
        self.maxlength = maxlength if maxlength is not None else minlength

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and len(value) > self.maxlength or len(value) < self.minlength:
            if self.minlength != self.maxlength:
                message = f'Length of value \'{value}\' at \'{key_path}\' should not be greater than {self.maxlength} or less than {self.minlength}.'
            else:
                message = f'Length of value \'{value}\' at \'{key_path}\' should be {self.minlength}.'
            raise ValidationException(
                {key_path: message},
                root
            )
