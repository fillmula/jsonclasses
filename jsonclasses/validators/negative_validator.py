"""module for negative validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class NegativeValidator(Validator):
    """Negative validator marks value valid for smaller than zero."""

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return ctx.value
        if ctx.value >= 0:
            kp = ctx.keypath_root
            v = ctx.value
            raise ValidationException(
                {kp: f'Value \'{v}\' at \'{kp}\' should be negative.'},
                ctx.root
            )
