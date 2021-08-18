"""module for alpha validator."""
from re import compile, match, IGNORECASE
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class AlphaValidator(Validator):
    """Alpha validator raises if value is not a alpha."""

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        if not value.isalpha():
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'product_name \'{value}\' at \'{kp}\' is not a alpha.'},
                context.root
            )
