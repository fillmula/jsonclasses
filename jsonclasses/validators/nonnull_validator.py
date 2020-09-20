"""module for nonnull validator."""
from typing import Any
from ..config import Config
from .validator import Validator
from ..utils.nonnull_note import NonnullNote


class NonnullValidator(Validator):
    """A nonnull validator transforms None into empty library."""

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:
        return NonnullNote() if value is None else value
