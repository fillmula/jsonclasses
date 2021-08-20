"""module for numeric validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class NumericValidator(Validator):
    """Numeric validator raises if value is not a numeric."""

    def validate(self, ctx: Ctx) -> None:
        if context.value is None:
            return
        value = context.value
        if not value.isnumeric():
            kp = context.keypath_root
            raise ValidationException(
                {kp: f'product_id \'{value}\' at \'{kp}\' is not a numeric.'},
                context.root
            )
