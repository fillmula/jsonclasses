"""module for trim validator."""
from typing import Any
from ..config import Config
from .validator import Validator


class TrimValidator(Validator):
    """Trim validator trims string values."""

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        if value is None:
            return None
        return value.strip()
