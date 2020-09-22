"""module for float validator."""
from typing import Any
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext, TransformingContext


class FloatValidator(Validator):
    """Date validator validate value against float type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.FLOAT

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if isinstance(context.value, float):
            return
        raise ValidationException(
            {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be float.'},
            context.root
        )

    def transform(self, context: TransformingContext) -> Any:
        if context.value is None:
            return None
        elif isinstance(context.value, int):
            return float(context.value)
        else:
            return context.value
