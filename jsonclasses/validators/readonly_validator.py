"""module for readonly validator."""
from typing import Any
from ..field_description import FieldDescription, WriteRule
from ..config import Config
from .validator import Validator


class ReadonlyValidator(Validator):
    """Readonly validator marks a field to be readonly."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.write_rule = WriteRule.NO_WRITE

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
