"""module for datetime validator."""
from typing import Any
from datetime import datetime
from ..fields import FieldType
from ..exceptions import ValidationException
from .type_validator import TypeValidator
from ..contexts import TransformingContext, ToJSONContext


class DatetimeValidator(TypeValidator):
    """Datetime validator validate value against datetime type."""

    def __init__(self):
        super().__init__()
        self.cls = datetime
        self.field_type = FieldType.DATETIME

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        elif isinstance(context.value, str):
            try:
                return datetime.fromisoformat(context.value.replace('Z', ''))
            except ValueError:
                raise ValidationException({
                    context.keypath_root: 'Datetime string format error.'
                }, context.root)
        else:
            return context.value

    def tojson(self, context: ToJSONContext) -> Any:
        if context.value is not None:
            return context.value.isoformat()[:23] + 'Z'
