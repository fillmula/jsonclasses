"""module for digit validator."""
from re import compile, match, IGNORECASE
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class DigitValidator(Validator):
    """Digit validator raises if value is not a digit."""

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        if not value.isdigit():
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'product_id \'{value}\' at \'{kp}\' is not a digit.'},
                context.root
            )
