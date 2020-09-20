"""module for match validator."""
from typing import Any
from re import search
from ..config import Config
from ..exceptions import ValidationException
from .validator import Validator


class MatchValidator(Validator):
    """Match validator validates value against pattern."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        if value is not None and search(self.pattern, value) is None:
            raise ValidationException(
                {key_path: f'Value \'{value}\' at \'{key_path}\' should match \'{self.pattern}\'.'},
                root
            )
