"""module for date validator."""
from typing import Any
from datetime import date, datetime
from ..field_definition import FieldType
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..contexts import TransformingContext, ToJSONContext


class DateValidator(TypeValidator):
    """Date validator validate value against date type."""

    def __init__(self):
        super().__init__()
        self.cls = date
        self.field_type = FieldType.DATE

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        elif isinstance(context.value, str):
            try:
                return date.fromisoformat(context.value[:10])
            except ValueError:
                raise ValidationException({
                    context.keypath_root: 'Date string format error.'
                }, context.root)
        elif type(context.value) == datetime:
            return date(context.value.year,
                        context.value.month,
                        context.value.day)
        else:
            return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is not None:
            return context.value.isoformat() + 'T00:00:00.000Z'
