"""module for numeric validator."""
from re import compile, match, IGNORECASE
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class NumericValidator(Validator):
    """Numeric validator raises if value is not a numeric."""

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return
        value = context.value
        if not value.isnumeric():
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'product_id \'{value}\' at \'{kp}\' is not a numeric.'},
                context.root
            )
