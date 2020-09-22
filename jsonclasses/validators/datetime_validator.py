"""module for datetime validator."""
from typing import Any
from datetime import datetime
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext, TransformingContext, ToJSONContext


class DatetimeValidator(Validator):
    """Datetime validator validate value against datetime type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.DATETIME

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if isinstance(context.value, datetime):
            return
        raise ValidationException(
            {
                context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be datetime.'
            },
            context.root
        )

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        elif isinstance(context.value, str):
            return datetime.fromisoformat(context.value.replace('Z', ''))
        else:
            return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is not None:
            return context.value.isoformat()[:23] + 'Z'
