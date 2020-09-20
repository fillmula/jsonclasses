"""module for default validator."""
from typing import Any
from ..config import Config
from .validator import Validator


class DefaultValidator(Validator):
    """Default validator assigns value a default value if value is `None`."""

    def __init__(self, default_value: Any) -> None:
        self.default_value = default_value

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        if value is None:
            if callable(self.default_value):
                return self.default_value()
            else:
                return self.default_value
        else:
            return value
