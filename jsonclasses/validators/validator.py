"""module for validator validator."""
from typing import Any
from ..field_definition import FieldDefinition
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class Validator:
    """Abstract and base class for validators."""

    def define(self, fdesc: FieldDefinition) -> None:
        """A hook and chance for validator to update field description."""

    def validate(self, context: ValidatingContext) -> None:
        """Validate the validity of the object."""

    def transform(self, context: TransformingContext) -> Any:
        """Transform raw input object into JSON Class acceptable object."""
        return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        """Transform JSON Class object and fields into JSON dict and values."""
        return context.value

    def serialize(self, context: TransformingContext) -> Any:
        """A chance for validators to update the object's value before the
        value is serialized into the database. This is only triggered for
        objects which are modified and have fields to write to the database.

        Unmodified objects won't cause serialize to trigger. JSON Classes which
        are not subclasses of ORMObject won't trigger this.
        """
        return context.value
