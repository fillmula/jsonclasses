"""module for validator validator."""
from typing import Any
from ..fields import FieldDescription
from ..config import Config
from ..exceptions import ValidationException
from ..contexts import ValidatingContext, TransformingContext


class Validator:
    """Abstract and base class for validators."""

    def define(self, field_description: FieldDescription) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, context: ValidatingContext) -> None:
        """Validate the validity of the object."""
        raise ValidationException(
            {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' is invalid.'},
            context.root
        )

    def transform(self, context: TransformingContext) -> Any:  # pylint: disable=unused-argument
        """Transform raw input object into JSON Class acceptable object."""
        return context.value

    def tojson(self, value: Any, config: Config) -> Any:  # pylint: disable=unused-argument
        """Transform JSON Class object and fields into JSON dict and values."""
        return value
