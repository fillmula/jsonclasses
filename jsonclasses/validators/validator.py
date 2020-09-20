"""module for validator validator."""
from typing import Any
from ..field_description import FieldDescription
from ..config import Config
from ..exceptions import ValidationException


class Validator:
    """Abstract and base class for validators."""

    def define(self, field_description: FieldDescription) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> None:
        """Validate the validity of the object."""
        raise ValidationException(
            {key_path: f'Value \'{value}\' at \'{key_path}\' is invalid.'},
            root
        )

    def transform(self, value: Any, key_path: str, root: Any, all_fields: bool, config: Config) -> Any:  # pylint: disable=unused-argument
        """Transform raw input object into JSON Class acceptable object."""
        return value

    def tojson(self, value: Any, config: Config) -> Any:  # pylint: disable=unused-argument
        """Transform JSON Class object and fields into JSON dict and values."""
        return value
