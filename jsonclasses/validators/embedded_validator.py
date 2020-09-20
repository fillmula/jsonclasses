"""module for embedded validator."""
from typing import Any
from ..field_description import FieldDescription, FieldStorage
from ..config import Config
from .validator import Validator


class EmbeddedValidator(Validator):
    """This validator marks value as embedded on the hosting object."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_storage = FieldStorage.EMBEDDED

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
