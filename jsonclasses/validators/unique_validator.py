"""module for unique validator."""
from typing import Any
from ..field_description import FieldDescription
from ..config import Config
from .validator import Validator


class UniqueValidator(Validator):
    """Unique validator marks a column should be unique."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.unique = True

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
