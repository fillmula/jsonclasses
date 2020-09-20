"""module for writeonly validator."""
from typing import Any
from ..field_description import FieldDescription, ReadRule
from ..config import Config
from .validator import Validator


class WriteonlyValidator(Validator):
    """Writeonly validator marks a field as writeonly."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.read_rule = ReadRule.NO_READ

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
