"""module for date validator."""
from typing import Any
from datetime import date
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class DateValidator(Validator):
    """Date validator validate value against date type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.DATE

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if isinstance(context.value, date):
            return
        raise ValidationException(
            {
                context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be date.'
            },
            context.root
        )

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        elif isinstance(context.value, str):
            return date.fromisoformat(context.value[:10])
        else:
            return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is not None:
            return context.value.isoformat() + 'T00:00:00.000Z'
