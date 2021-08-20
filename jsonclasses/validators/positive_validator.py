"""module for positive validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import VCtx


class PositiveValidator(Validator):
    """Positive validator marks value valid for large than zero."""

    def validate(self, context: VCtx) -> None:
        if context.value is None:
            return context.value
        if context.value <= 0:
            kp = context.keypath_root
            v = context.value
            raise ValidationException(
                {kp: f'Value \'{v}\' at \'{kp}\' should be positive.'},
                context.root
            )
