"""module for transform validator."""
from typing import Callable, Any
from ..config import Config
from .validator import Validator


class TransformValidator(Validator):
    """Transform validator transforms value."""

    def __init__(self, transformer: Callable) -> None:
        self.transformer = transformer

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        if value is not None:
            return self.transformer(value)
        else:
            return None
