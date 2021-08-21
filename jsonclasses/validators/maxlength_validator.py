"""module for maxlength validator."""
from ..exceptions import ValidationException
from .validator import Validator
from ..ctx import Ctx


class MaxlengthValidator(Validator):
    """Maxlength validator validates value against max length."""

    def __init__(self, maxlength: int) -> None:
        self.maxlength = maxlength

    def validate(self, ctx: Ctx) -> None:
        if ctx.value is None:
            return
        if len(ctx.value) > self.maxlength:
            raise ValidationException(
                {ctx.keypath_root: f'Length of value \'{ctx.value}\' at \'{ctx.keypath_root}\' should not be greater than {self.maxlength}.'},
                ctx.root
            )
