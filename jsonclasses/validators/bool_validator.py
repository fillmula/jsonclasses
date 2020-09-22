"""module for bool validator."""
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class BoolValidator(Validator):
    """Bool validator validate value against bool."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.BOOL

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if isinstance(context.value, bool):
            return
        raise ValidationException(
            {
                context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be bool.'
            },
            context.root
        )
