"""module for maxlength validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class MaxlengthValidator(Validator):
    """Maxlength validator validates value against max length."""

    def __init__(self, maxlength: int) -> None:
        self.maxlength = maxlength

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if len(context.value) > self.maxlength:
            raise ValidationException(
                {context.keypath_root: f'Length of value \'{context.value}\' at \'{context.keypath_root}\' should not be greater than {self.maxlength}.'},
                context.root
            )
