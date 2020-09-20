"""module for writeonce validator."""
from typing import Any
from ..field_description import FieldDescription, WriteRule
from ..config import Config
from .validator import Validator


class WriteonceValidator(Validator):
    """Writeonce validator marks a field as writeonce."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.WRITE_ONCE

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
