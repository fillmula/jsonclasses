"""module for linkto validator."""
from typing import Any
from ..field_description import FieldDescription, FieldStorage
from ..config import Config
from .validator import Validator


class LinkToValidator(Validator):
    """Link to validator marks a field which is a local key."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.LOCAL_KEY

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
