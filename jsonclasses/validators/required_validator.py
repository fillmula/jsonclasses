"""module for required validator."""
from ..fields import FieldDescription
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class RequiredValidator(Validator):
    """Mark a field as required."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.required = True

    def validate(self, context: ValidatingContext) -> None:
        if context.value is not None:
            return
        raise ValidationException(
            {context.keypath: f'Value at \'{context.keypath}\' should not be None.'},
            context.root
        )
