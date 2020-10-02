"""module for minlength validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class MinlengthValidator(Validator):
    """Minlength validator validates value against min length."""

    def __init__(self, minlength: int) -> None:
        self.minlength = minlength

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        if len(context.value) < self.minlength:
            raise ValidationException(
                {context.keypath_root: f'Length of value \'{context.value}\' at \'{context.keypath_root}\' should not be less than {self.minlength}.'},
                context.root
            )
