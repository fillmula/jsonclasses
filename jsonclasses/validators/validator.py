"""module for validator validator."""
from typing import Any
from ..fields import FieldDescription
from ..exceptions import ValidationException
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


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

    def transform(self, context: TransformingContext) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return context.value
