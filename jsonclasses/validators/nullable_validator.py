"""module for nullable validator."""
from typing import Any
from ..field_description import FieldDescription, CollectionNullability
from ..config import Config
from .validator import Validator


class NullableValidator(Validator):
    """A nullable validator marks a collection item field to be nullable."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.collection_nullability = CollectionNullability.NULLABLE

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        pass
