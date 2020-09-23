"""module for validator validator."""
from typing import Any
from ..fields import FieldDescription
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class Validator:
    """Abstract and base class for validators."""

    def define(self, field_description: FieldDescription) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, context: ValidatingContext) -> None:
        """Validate the validity of the object."""

    def transform(self, context: TransformingContext) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return context.value
