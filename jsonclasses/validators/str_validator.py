"""module for str validator."""
from ..fields import FieldDescription, FieldType
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class StrValidator(Validator):
    """Str validator validates value against str type."""

    def define(self, field_description: FieldDescription) -> None:
        field_description.field_type = FieldType.STR

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if isinstance(context.value, str):
            return
        raise ValidationException(
            {context.keypath: f'Value \'{context.value}\' at \'{context.keypath}\' should be str.'},
            context.root
        )
