"""module for max validator."""
from typing import Any, Union
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class MaxValidator(Validator):
    """Match validator validates value against max value."""

    def __init__(self, max_value: Union[int, float]) -> None:
        self.max_value = max_value

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and value > self.max_value:
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should not be greater than {self.max_value}.'},
                root
            )
