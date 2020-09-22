"""module for int validator."""
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class IntValidator(Validator):
    """Int validator validate value against int type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.INT

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if type(context.value) is int:  # bool will test True for isinstance
            return
        raise ValidationException(
            {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be int.'},
            context.root
        )
