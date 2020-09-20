"""module for linkedthru validator."""
from typing import Any
from ..field_description import FieldDescription, FieldStorage
from ..config import Config
from .validator import Validator


class LinkedThruValidator(Validator):
    """Linked by validator marks a field linked with a joinning table."""

    def __init__(self, foreign_key: str) -> None:
        self.foreign_key = foreign_key

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.FOREIGN_KEY
        field_description.foreign_key = self.foreign_key
        field_description.use_join_table = True

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
