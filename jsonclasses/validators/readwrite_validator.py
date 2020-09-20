"""module for readwrite validator."""
from typing import Any
from ..field_description import FieldDescription, WriteRule, ReadRule
from ..config import Config
from .validator import Validator


class ReadwriteValidator(Validator):
    """Readwrite validator marks a field both readable and writable."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.UNLIMITED
        field_description.read_rule = ReadRule.UNLIMITED

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
