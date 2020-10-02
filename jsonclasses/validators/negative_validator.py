"""module for negative validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..contexts import ValidatingContext


class NegativeValidator(Validator):
    """Negative validator marks value valid for smaller than zero."""

    def validate(self, context: ValidatingContext) -> None:
        if context.value is None:
            return context.value
        if context.value >= 0:
            kp = context.keypath_root
            v = context.value
            raise ValidationException(
                {kp: f'Value \'{v}\' at \'{kp}\' should be negative.'},
                context.root
            )
