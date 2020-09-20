"""module for truncate validator."""
from typing import Any
from ..config import Config
from .validator import Validator


class TruncateValidator(Validator):
    """Truncate validator truncates value."""

    def __init__(self, max_length: int) -> None:
        self.max_length = max_length

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        if value is not None and value.__len__() > self.max_length:
            return value[:self.max_length]
        else:
            return value
