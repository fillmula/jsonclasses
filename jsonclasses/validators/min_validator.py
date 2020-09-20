"""module for min validator."""
from typing import Any, Union
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class MinValidator(Validator):
    """Match validator validates value against min value."""

    def __init__(self, min_value: Union[int, float]):
        self.min_value = min_value

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and value < self.min_value:
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should not be less than {self.min_value}.'},
                root
            )
